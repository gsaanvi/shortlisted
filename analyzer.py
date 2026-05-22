# analyzer.py
# ─────────────────────────────────────────────
# Shortlisted — Core analysis engine
# ─────────────────────────────────────────────

# analyzer.py
import re
from utils import (
    extract_skills_from_text,
    get_keyword_category,
)


def analyze_keywords(resume_text, jd_text):
    """
    Extract skills from JD, check each against resume.
    Uses canonical skill names so no duplicates ever.
    """
    jd_skills = extract_skills_from_text(jd_text)
    resume_skills = extract_skills_from_text(resume_text)

    matched = {}
    missing = {}

    for skill, count in jd_skills.items():
        priority = 'high' if count >= 2 else 'standard'
        category = get_keyword_category(skill)
        entry = {
            'priority': priority,
            'category': category,
            'count': count,
        }
        if skill in resume_skills:
            matched[skill] = entry
        else:
            missing[skill] = entry

    return matched, missing


def calculate_score(matched, missing):
    """
    Weighted score: high priority = 2x, standard = 1x
    """
    matched_weight = sum(
        2 if i['priority'] == 'high' else 1
        for i in matched.values()
    )
    total_weight = matched_weight + sum(
        2 if i['priority'] == 'high' else 1
        for i in missing.values()
    )
    if total_weight == 0:
        return 0.0
    return round((matched_weight / total_weight) * 100, 1)


def apply_cap(score, missing):
    high_missing = sum(
        1 for i in missing.values() if i['priority'] == 'high'
    )
    capped = False
    if high_missing > 5 and score > 60:
        score = 60.0
        capped = True
    return round(score, 1), capped, high_missing


def group_by_category(keywords_dict):
    groups = {'technical': [], 'experience': [], 'soft': [], 'other': []}
    for kw, info in keywords_dict.items():
        groups[info['category']].append({
            'keyword': kw,
            'priority': info['priority'],
        })
    for cat in groups:
        groups[cat].sort(key=lambda x: (x['priority'] != 'high', x['keyword']))
    return groups


def check_formatting_issues(resume_text):
    issues = []
    word_count = len(resume_text.split())
    resume_lower = resume_text.lower()

    if word_count < 100:
        issues.append({'type': 'error',
            'message': f'Resume too short ({word_count} words). Aim for at least 300 words.'})
    elif word_count > 1000:
        issues.append({'type': 'info',
            'message': f'Resume is long ({word_count} words). Ideal is 400–700 words.'})

    if not re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text):
        issues.append({'type': 'error',
            'message': 'No email detected. Make sure it is plain text not inside an image or header.'})

    if not re.search(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', resume_text):
        issues.append({'type': 'warning',
            'message': 'No phone number detected. Ensure contact info is in plain text.'})

    missing_sections = [
        s for s in ['education', 'experience', 'skills']
        if s not in resume_lower
    ]
    if missing_sections:
        issues.append({'type': 'warning',
            'message': f'Missing section headers: {", ".join(s.title() for s in missing_sections)}.'})

    if not any(c in resume_text for c in ['•', '-', '●', '·']):
        issues.append({'type': 'warning',
            'message': 'No bullet points detected. Use • or - to list responsibilities.'})

    if len(re.findall(r'\b\d+[\%\+]?\b', resume_text)) < 3:
        issues.append({'type': 'info',
            'message': 'Few metrics found. Add numbers — e.g. "Improved performance by 40%", "Served 10,000 users".'})

    weak = [w for w in ['responsible for', 'helped with', 'assisted in'] if w in resume_lower]
    if weak:
        issues.append({'type': 'info',
            'message': f'Weak phrase: "{weak[0]}". Use action verbs: Built, Developed, Led, Optimized, Delivered.'})

    return issues


def generate_suggestions(matched, missing, score, capped, high_missing):
    suggestions = []

    if score >= 75:
        suggestions.append(
            f"Strong match at {score}%. Your resume aligns well with this role. "
            f"Focus on quantifying achievements with numbers and impact metrics."
        )
    elif score >= 50:
        suggestions.append(
            f"Moderate match at {score}%. You have relevant experience but are missing "
            f"some key skills. Adding the missing high-priority keywords should push "
            f"you above the ATS cutoff."
        )
    else:
        suggestions.append(
            f"Weak match at {score}%. Your resume needs skill alignment. "
            f"Focus on the missing high-priority technical skills first."
        )

    if capped:
        suggestions.append(
            f"Score was capped — {high_missing} critical skills are missing. "
            f"These appear multiple times in the JD meaning the employer "
            f"considers them essential."
        )

    hi_tech = [
        kw for kw, i in missing.items()
        if i['priority'] == 'high' and i['category'] == 'technical'
    ]
    if hi_tech:
        kw_list = ', '.join(f'"{k}"' for k in hi_tech[:5])
        suggestions.append(
            f"Critical technical skills missing (appear 2+ times in JD): {kw_list}. "
            f"Add these to your Skills section if you have experience with them."
        )

    std_tech = [
        kw for kw, i in missing.items()
        if i['priority'] == 'standard' and i['category'] == 'technical'
    ]
    if std_tech:
        kw_list = ', '.join(f'"{k}"' for k in std_tech[:4])
        suggestions.append(
            f"Other technical skills from JD not in resume: {kw_list}. "
            f"Add these if applicable."
        )

    exp_missing = [
        kw for kw, i in missing.items()
        if i['category'] == 'experience'
    ]
    if exp_missing:
        kw_list = ', '.join(exp_missing[:3])
        suggestions.append(
            f"Experience terms missing: {kw_list}. "
            f"Mirror the exact language the JD uses."
        )

    suggestions.append(
        "Add measurable achievements — e.g. 'Reduced load time by 35%', "
        "'Built system serving 5,000 daily users'. Numbers strengthen "
        "both ATS and human review."
    )

    return suggestions


def run_full_analysis(resume_text, jd_text):
    matched, missing = analyze_keywords(resume_text, jd_text)
    score = calculate_score(matched, missing)
    final_score, capped, high_missing = apply_cap(score, missing)

    # ── NEW: Extra skills in resume but not required by JD ──
    from utils import extract_skills_from_text
    resume_skills = extract_skills_from_text(resume_text)
    jd_skill_names = set(matched.keys()) | set(missing.keys())
    extra_skills = [
        skill for skill in resume_skills
        if skill not in jd_skill_names
    ]
    extra_skills.sort()

    # ── NEW: Summary line ──
    total_jd = len(matched) + len(missing)
    summary_line = (
        f"Your resume covers {len(matched)} of {total_jd} "
        f"skills this role asks for"
        + (f", plus {len(extra_skills)} additional skill"
           f"{'s' if len(extra_skills) != 1 else ''} not required by this JD."
           if extra_skills else ".")
    )

    # ── NEW: All JD skills sorted by priority then name ──
    # High priority first, within each group ✅ before ❌
    all_jd_skills = []
    for kw, info in sorted(
        {**matched, **missing}.items(),
        key=lambda x: (x[1]['priority'] != 'high', x[0])
    ):
        all_jd_skills.append({
            'keyword': kw,
            'found': kw in matched,
            'priority': info['priority'],
            'category': info['category'],
        })

    return {
        'combined_score': final_score,
        'ats_score': final_score,
        'role_fit_score': final_score,
        'capped': capped,
        'high_priority_missing': high_missing,
        'matched': matched,
        'missing': missing,
        'matched_by_category': group_by_category(matched),
        'missing_by_category': group_by_category(missing),
        'formatting_issues': check_formatting_issues(resume_text),
        'suggestions': generate_suggestions(
            matched, missing, final_score, capped, high_missing
        ),
        'total_matched': len(matched),
        'total_missing': len(missing),
        # New fields
        'all_jd_skills': all_jd_skills,
        'extra_skills': extra_skills,
        'summary_line': summary_line,
    }