# utils.py
# ─────────────────────────────────────────────
# Shortlisted — PDF reading and keyword utilities
# ─────────────────────────────────────────────

# utils.py
import pdfplumber
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))

# Generic words that are nouns but not skills
# EXTRA_STOPWORDS = {
#     'application', 'applications', 'system', 'systems', 'service', 'services',
#     'solution', 'solutions', 'software', 'technology', 'technologies',
#     'framework', 'frameworks', 'platform', 'platforms', 'environment',
#     'tool', 'tools', 'code', 'coding', 'codebase', 'standard', 'standards',
#     'practice', 'practices', 'process', 'processes', 'project', 'projects',
#     'product', 'products', 'business', 'client', 'clients', 'customer',
#     'user', 'users', 'team', 'teams', 'member', 'members', 'role', 'roles',
#     'candidate', 'position', 'company', 'organization', 'industry',
#     'experience', 'skill', 'skills', 'knowledge', 'ability', 'understanding',
#     'proficiency', 'expertise', 'familiarity', 'requirement', 'requirements',
#     'responsibility', 'responsibilities', 'opportunity', 'benefit', 'benefits',
#     'year', 'years', 'month', 'months', 'day', 'days', 'time', 'date',
#     'work', 'working', 'job', 'career', 'field', 'area', 'domain',
#     'feature', 'features', 'issue', 'issues', 'problem', 'problems',
#     'task', 'tasks', 'goal', 'goals', 'result', 'results', 'output',
#     'quality', 'performance', 'efficiency', 'reliability', 'scalability',
#     'security', 'maintenance', 'development', 'implementation', 'integration',
#     'management', 'analysis', 'design', 'testing', 'deployment', 'monitoring',
#     'documentation', 'communication', 'collaboration', 'coordination',
#     'bachelor', 'master', 'degree', 'science', 'engineering', 'computer',
#     'information', 'data', 'database', 'network', 'web', 'mobile', 'cloud',
#     'api', 'apis', 'interface', 'architecture', 'infrastructure',
#     'salary', 'package', 'benefit', 'location', 'remote', 'hybrid', 'office',
# }

# Known tech skills with all their variations mapped to one canonical form
SKILL_VARIATIONS = {
    'python': ['python'],
    'java': ['java'],
    'javascript': ['javascript', 'js'],
    'typescript': ['typescript', 'ts'],
    'cpp': ['c++', 'cpp'],
    'csharp': ['c#', 'csharp'],
    'golang': ['golang', 'go lang'],
    'ruby': ['ruby'],
    'rust': ['rust'],
    'swift': ['swift'],
    'kotlin': ['kotlin'],
    'scala': ['scala'],
    'html': ['html', 'html5'],
    'css': ['css', 'css3'],
    'react': ['react', 'reactjs', 'react.js'],
    'angular': ['angular', 'angularjs'],
    'vue': ['vue', 'vuejs', 'vue.js'],
    'nodejs': ['node.js', 'nodejs', 'node js'],
    'nextjs': ['next.js', 'nextjs'],
    'django': ['django'],
    'flask': ['flask'],
    'fastapi': ['fastapi', 'fast api'],
    'spring': ['spring', 'spring boot'],
    'express': ['express', 'expressjs'],
    'sql': ['sql'],
    'mysql': ['mysql'],
    'postgresql': ['postgresql', 'postgres'],
    'mongodb': ['mongodb', 'mongo'],
    'redis': ['redis'],
    'nosql': ['nosql', 'no-sql', 'no sql'],
    'elasticsearch': ['elasticsearch', 'elastic search'],
    'aws': ['aws', 'amazon web services'],
    'azure': ['azure', 'microsoft azure'],
    'gcp': ['gcp', 'google cloud'],
    'docker': ['docker'],
    'kubernetes': ['kubernetes', 'k8s'],
    'git': ['git'],
    'github': ['github'],
    'gitlab': ['gitlab'],
    'jenkins': ['jenkins'],
    'cicd': ['ci/cd', 'cicd', 'ci cd'],
    'linux': ['linux'],
    'bash': ['bash', 'shell scripting'],
    'terraform': ['terraform'],
    'devops': ['devops'],
    'tensorflow': ['tensorflow'],
    'pytorch': ['pytorch'],
    'pandas': ['pandas'],
    'numpy': ['numpy'],
    'sklearn': ['scikit-learn', 'sklearn'],
    'tableau': ['tableau'],
    'powerbi': ['power bi', 'powerbi'],
    'spark': ['apache spark', 'spark'],
    'hadoop': ['hadoop'],
    'rest api': ['rest api', 'rest apis', 'restful api', 'restful apis',
                 'restful', 'rest services'],
    'graphql': ['graphql'],
    'microservices': ['microservices', 'micro services'],
    'machine learning': ['machine learning', 'ml'],
    'deep learning': ['deep learning', 'dl'],
    'nlp': ['nlp', 'natural language processing'],
    'computer vision': ['computer vision', 'cv'],
    'data science': ['data science'],
    'data analysis': ['data analysis', 'data analytics'],
    'statistics': ['statistics', 'statistical'],
    'agile': ['agile', 'agile methodology', 'agile framework'],
    'scrum': ['scrum'],
    'figma': ['figma'],
    'jira': ['jira'],
    'postman': ['postman'],
    'excel': ['excel', 'ms excel'],
    'algorithms': ['algorithms', 'data structures', 'dsa'],
    'problem solving': ['problem solving', 'problem-solving'],
    'communication': ['communication', 'communicator'],
    'fast learner': ['fast learner', 'quick learner'],
}

# Build reverse map: variant → canonical
VARIANT_TO_CANONICAL = {}
for canonical, variants in SKILL_VARIATIONS.items():
    for variant in variants:
        VARIANT_TO_CANONICAL[variant.lower()] = canonical

# All canonical skill names
ALL_SKILLS = set(SKILL_VARIATIONS.keys())

# Display categories
TECHNICAL_SKILLS = {
    'python', 'java', 'javascript', 'typescript', 'cpp', 'csharp',
    'golang', 'ruby', 'rust', 'swift', 'kotlin', 'scala',
    'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'nextjs',
    'django', 'flask', 'fastapi', 'spring', 'express',
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'nosql', 'elasticsearch',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github', 'gitlab',
    'jenkins', 'cicd', 'linux', 'bash', 'terraform', 'devops',
    'tensorflow', 'pytorch', 'pandas', 'numpy', 'sklearn',
    'tableau', 'powerbi', 'spark', 'hadoop', 'excel',
    'rest api', 'graphql', 'microservices',
    'machine learning', 'deep learning', 'nlp', 'computer vision',
    'data science', 'data analysis', 'statistics', 'algorithms',
    'agile', 'scrum', 'figma', 'jira', 'postman',
}

EXPERIENCE_KEYWORDS = {
    'backend', 'frontend', 'full stack',
    'leadership', 'mentoring', 'management',
}

SOFT_SKILLS = {
    'communication', 'collaboration', 'teamwork',
    'problem solving', 'critical thinking', 'adaptability',
    'fast learner',
}


def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def normalize_text(text):
    """Lowercase and normalize whitespace."""
    return re.sub(r'\s+', ' ', text.lower().strip())


def extract_skills_from_text(text):
    """
    Extracts known skills from text using variant matching.
    Returns dict: canonical_skill -> count
    This handles all variations automatically via VARIANT_TO_CANONICAL map.
    """
    text_lower = normalize_text(text)
    found = {}

    # Check multi-word variants first (longer ones first to avoid partial matches)
    all_variants = sorted(VARIANT_TO_CANONICAL.keys(), key=len, reverse=True)

    for variant in all_variants:
        pattern = r'\b' + re.escape(variant) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            canonical = VARIANT_TO_CANONICAL[variant]
            # Only count if not already found via another variant
            if canonical not in found:
                found[canonical] = len(matches)
            else:
                found[canonical] += len(matches)

    return found


def get_keyword_category(keyword):
    kw = keyword.lower()
    if kw in TECHNICAL_SKILLS:
        return 'technical'
    elif kw in EXPERIENCE_KEYWORDS:
        return 'experience'
    elif kw in SOFT_SKILLS:
        return 'soft'
    return 'other'