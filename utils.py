# Shortlisted — PDF reading and keyword utilities

import pdfplumber
import re
import nltk

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
STOPWORDS = set(stopwords.words('english'))


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


SKILL_VARIATIONS = {
    # Languages
    'python': ['python'],
    'java': ['java'],
    'javascript': ['javascript', 'js'],
    'typescript': ['typescript', 'ts'],
    'cpp': ['c++', 'cpp'],
    'csharp': ['c#', 'csharp'],
    'golang': ['golang', 'go lang', 'go'],
    'ruby': ['ruby'],
    'rust': ['rust'],
    'swift': ['swift'],
    'kotlin': ['kotlin'],
    'scala': ['scala'],
    'php': ['php'],
    'r': ['r programming', 'r language'],
    'matlab': ['matlab'],
    'perl': ['perl'],
    'dart': ['dart'],

    # Frontend
    'html': ['html', 'html5'],
    'css': ['css', 'css3'],
    'react': ['react', 'reactjs', 'react.js'],
    'angular': ['angular', 'angularjs'],
    'vue': ['vue', 'vuejs', 'vue.js'],
    'nextjs': ['next.js', 'nextjs', 'next js'],
    'nuxtjs': ['nuxt.js', 'nuxtjs'],
    'svelte': ['svelte'],
    'tailwind': ['tailwind', 'tailwindcss', 'tailwind css'],
    'bootstrap': ['bootstrap'],
    'jquery': ['jquery'],
    'redux': ['redux'],
    'webpack': ['webpack'],
    'vite': ['vite'],
    'sass': ['sass', 'scss'],
    'typescript': ['typescript', 'ts'],
    'three.js': ['three.js', 'threejs'],

    # Backend 
    'nodejs': ['node.js', 'nodejs', 'node js'],
    'django': ['django'],
    'flask': ['flask'],
    'fastapi': ['fastapi', 'fast api'],
    'spring': ['spring', 'spring boot', 'springboot'],
    'express': ['express', 'expressjs', 'express.js'],
    'laravel': ['laravel'],
    'rails': ['rails', 'ruby on rails'],
    'dotnet': ['.net', 'dotnet', 'asp.net'],
    'graphql': ['graphql'],
    'rest api': ['rest api', 'rest apis', 'restful api', 'restful apis', 'restful', 'rest services'],
    'grpc': ['grpc'],
    'websocket': ['websocket', 'websockets'],
    'microservices': ['microservices', 'micro services'],

    # Databases
    'sql': ['sql'],
    'mysql': ['mysql'],
    'postgresql': ['postgresql', 'postgres'],
    'mongodb': ['mongodb', 'mongo'],
    'redis': ['redis'],
    'nosql': ['nosql', 'no-sql', 'no sql'],
    'elasticsearch': ['elasticsearch', 'elastic search'],
    'sqlite': ['sqlite'],
    'oracle': ['oracle', 'oracle db'],
    'cassandra': ['cassandra', 'apache cassandra'],
    'dynamodb': ['dynamodb', 'dynamo db'],
    'firebase': ['firebase'],
    'supabase': ['supabase'],
    'prisma': ['prisma'],
    'sequelize': ['sequelize'],

    # Cloud & DevOps
    'aws': ['aws', 'amazon web services'],
    'azure': ['azure', 'microsoft azure'],
    'gcp': ['gcp', 'google cloud', 'google cloud platform'],
    'docker': ['docker'],
    'kubernetes': ['kubernetes', 'k8s'],
    'git': ['git'],
    'github': ['github'],
    'gitlab': ['gitlab'],
    'jenkins': ['jenkins'],
    'cicd': ['ci/cd', 'cicd', 'ci cd', 'continuous integration', 'continuous deployment'],
    'linux': ['linux', 'ubuntu', 'unix'],
    'bash': ['bash', 'shell scripting', 'shell script'],
    'terraform': ['terraform'],
    'devops': ['devops'],
    'ansible': ['ansible'],
    'nginx': ['nginx'],
    'apache': ['apache'],
    'heroku': ['heroku'],
    'vercel': ['vercel'],
    'netlify': ['netlify'],
    'cloudflare': ['cloudflare'],
    'github actions': ['github actions'],
    'bitbucket': ['bitbucket'],
    'prometheus': ['prometheus'],
    'grafana': ['grafana'],

    # Data & ML & AI
    'tensorflow': ['tensorflow'],
    'pytorch': ['pytorch'],
    'keras': ['keras'],
    'sklearn': ['scikit-learn', 'sklearn'],
    'pandas': ['pandas'],
    'numpy': ['numpy'],
    'matplotlib': ['matplotlib'],
    'seaborn': ['seaborn'],
    'plotly': ['plotly'],
    'scipy': ['scipy'],
    'opencv': ['opencv', 'cv2'],
    'hugging face': ['hugging face', 'huggingface'],
    'langchain': ['langchain'],
    'openai': ['openai', 'chatgpt api', 'gpt'],
    'machine learning': ['machine learning', 'ml'],
    'deep learning': ['deep learning', 'dl'],
    'nlp': ['nlp', 'natural language processing'],
    'computer vision': ['computer vision'],
    'data science': ['data science'],
    'data analysis': ['data analysis', 'data analytics'],
    'statistics': ['statistics', 'statistical analysis'],
    'algorithms': ['algorithms', 'data structures', 'dsa'],
    'tableau': ['tableau'],
    'powerbi': ['power bi', 'powerbi'],
    'spark': ['apache spark', 'spark', 'pyspark'],
    'hadoop': ['hadoop'],
    'airflow': ['airflow', 'apache airflow'],
    'kafka': ['kafka', 'apache kafka'],
    'excel': ['excel', 'ms excel', 'microsoft excel'],
    'looker': ['looker'],
    'databricks': ['databricks'],
    'snowflake': ['snowflake'],
    'etl': ['etl', 'extract transform load'],

    # Mobile
    'react native': ['react native'],
    'flutter': ['flutter'],
    'android': ['android', 'android development'],
    'ios': ['ios', 'ios development'],
    'swift': ['swift'],
    'kotlin': ['kotlin'],

    # Testing
    'selenium': ['selenium'],
    'cypress': ['cypress'],
    'jest': ['jest'],
    'pytest': ['pytest'],
    'junit': ['junit'],
    'postman': ['postman'],
    'unit testing': ['unit testing', 'unit test'],

    # Tools & Practices
    'agile': ['agile', 'agile methodology'],
    'scrum': ['scrum'],
    'jira': ['jira'],
    'figma': ['figma'],
    'git': ['git'],
    'linux': ['linux'],
    'microservices': ['microservices'],
    'system design': ['system design'],
    'object oriented': ['object oriented', 'oop', 'oops'],
    'data structures': ['data structures', 'dsa'],
    'problem solving': ['problem solving', 'problem-solving'],
    'communication': ['communication'],
    'teamwork': ['teamwork'],
    'fast learner': ['fast learner', 'quick learner'],
    'blockchain': ['blockchain', 'web3', 'solidity'],
    'embedded': ['embedded', 'embedded systems'],
    'iot': ['iot', 'internet of things'],
    'cybersecurity': ['cybersecurity', 'cyber security', 'information security'],
    'networking': ['networking', 'computer networks', 'tcp/ip'],
}

# reverse map: variant → canonical
VARIANT_TO_CANONICAL = {}
for canonical, variants in SKILL_VARIATIONS.items():
    for variant in variants:
        VARIANT_TO_CANONICAL[variant.lower()] = canonical

# All canonical skill names
ALL_SKILLS = set(SKILL_VARIATIONS.keys())


TECHNICAL_SKILLS = {
    # Languages
    'python', 'java', 'javascript', 'typescript', 'cpp', 'csharp',
    'golang', 'ruby', 'rust', 'swift', 'kotlin', 'scala', 'php',
    'r', 'matlab', 'perl', 'dart',
    # Frontend
    'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'nextjs',
    'nuxtjs', 'svelte', 'tailwind', 'bootstrap', 'jquery', 'redux',
    'webpack', 'vite', 'sass', 'three.js',
    # Backend
    'django', 'flask', 'fastapi', 'spring', 'express', 'laravel',
    'rails', 'dotnet', 'graphql', 'rest api', 'grpc', 'websocket',
    'microservices',
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'nosql',
    'elasticsearch', 'sqlite', 'oracle', 'cassandra', 'dynamodb',
    'firebase', 'supabase', 'prisma', 'sequelize',
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git', 'github',
    'gitlab', 'jenkins', 'cicd', 'linux', 'bash', 'terraform',
    'devops', 'ansible', 'nginx', 'apache', 'heroku', 'vercel',
    'netlify', 'cloudflare', 'github actions', 'bitbucket',
    'prometheus', 'grafana',
    # Data & ML & AI
    'tensorflow', 'pytorch', 'keras', 'sklearn', 'pandas', 'numpy',
    'matplotlib', 'seaborn', 'plotly', 'scipy', 'opencv',
    'hugging face', 'langchain', 'openai',
    'machine learning', 'deep learning', 'nlp', 'computer vision',
    'data science', 'data analysis', 'statistics', 'algorithms',
    'tableau', 'powerbi', 'spark', 'hadoop', 'airflow', 'kafka',
    'excel', 'looker', 'databricks', 'snowflake', 'etl',
    # Mobile
    'react native', 'flutter', 'android', 'ios',
    # Testing
    'selenium', 'cypress', 'jest', 'pytest', 'junit', 'postman',
    'unit testing',
    # Tools & Practices
    'agile', 'scrum', 'jira', 'figma',
    'system design', 'object oriented', 'data structures',
    'blockchain', 'embedded', 'iot', 'cybersecurity', 'networking',
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
    handles all variations automatically via VARIANT_TO_CANONICAL map.
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