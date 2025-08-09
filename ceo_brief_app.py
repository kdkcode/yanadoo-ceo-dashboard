from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ceo-brief-secret-key'

# 데이터 파일 경로
CEO_DATA_FILE = 'ceo_brief_data.json'

# 기본 데이터 구조 (CEO 브리핑용 - S급 인재 양성 중심)
DEFAULT_CEO_DATA = {
    "header": {
        "title": "야나두 AI서포트팀 – S급 인재 양성 전략",
        "subtitle": "AI 내재화를 통한 핵심 성과 및 인재 육성 현황",
        "report_date": "2025년 7월 말"
    },
    "kpis": {
        "s_grade_talent": {
            "label": "S급 인재 현황",
            "value": "1명 → 6명 목표",
            "detail": "코너 + 5명 추가 양성 목표",
            "current": 1,
            "target": 6,
            "achievement_rate": 16.7
        },
        "flow_success": {
            "label": "Flow 대박 성과",
            "value": "2,132만 조회수",
            "detail": "ROI 2,797% | 8만 팔로워 증가",
            "views": 21320000,
            "roi": 2797,
            "followers": 80000
        },
        "ai_efficiency": {
            "label": "AI 업무 효율 향상",
            "value": "평균 85% 향상",
            "detail": "PPT 6h절감, TM 30분절감",
            "avg_improvement": 85,
            "departments": 7
        },
        "cost_optimization": {
            "label": "비용 최적화",
            "value": "₩534,586 절감",
            "detail": "46.2% 절감 | 32개→17개 도구",
            "saved_amount": 534586,
            "reduction_rate": 46.2
        }
    },
    "objectives": {
        "why": "AI로 압도적 성과를 낸 S급 인재를 각 부서에 양성하여 전사 생산성과 창의력을 극대화한다.",
        "what": "Flow 성공사례를 모델로 한 S급 인재 양성 프로그램과 AI 내재화 4가지 핵심 질문 체계화",
        "how": "AI 효율성 측정 → 추가 가치 창출 → 고유 역량 강화 → 인력 최적화 4단계 성장 로드맵 구축"
    },
    "ai_core_questions": [
        {
            "question": "AI(또는 자동화 도구)를 통해 현재 업무 효율을 몇 % 향상시켰나요?",
            "purpose": "정량적 효율성 측정",
            "example": "PPT 제작 시간 75% 단축 (8h → 2h)"
        },
        {
            "question": "그렇게 확보된 시간을 활용하여 어떤 추가적인 업무나 가치 창출을 했나요?",
            "purpose": "부가가치 창출 확인",
            "example": "절약된 6시간으로 신규 전략 기획 및 고도화"
        },
        {
            "question": "AI가 대체를 못하는 개인의 역량을 설명하세요.",
            "purpose": "고유 가치 인식",
            "example": "창의적 콘텐츠 기획, 고객 감정 이해, 전략적 판단"
        },
        {
            "question": "추가 인력 지원이 필요하다면, AI로 수행 못하는 이유를 설명해 주세요.",
            "purpose": "인력 최적화 근거",
            "example": "복잡한 이해관계자 협상, 위기상황 대응, 혁신적 아이디어 구상"
        }
    ],
    "flow_success_case": {
        "employee": "코너 (마케팅팀)",
        "tool": "Flow (Hailou AI Video)",
        "achievement": "9개 영상으로 인스타그램 대박",
        "instagram_views": "2,132만 조회수",
        "follower_growth": "8만 팔로워 증가",
        "efficiency_gain": "97%",
        "cost_replacement": "기존 영상 제작비 ₩720만 절감",
        "roi": "2,797%",
        "unique_capability": "트렌드 감각, 바이럴 콘텐츠 기획력, 고객 감정 이해",
        "s_grade_evidence": "영상당 237만회 조회로 업계 최고 수준 달성",
        "why_human_needed": "AI는 템플릿 생성만 가능, 바이럴 요소 감각과 타이밍은 인간만 가능"
    },
    "current_s_grade_status": {
        "current_count": 1,
        "target_count": 6,
        "target_description": "코너(S급) + 5명 추가 양성으로 총 6명 목표",
        "flow_model": "Flow 성공사례를 모델로 전사 확산"
    },
    "dept_ai_status": [
        {
            "department": "마케팅팀",
            "s_grade_count": 1,
            "s_grade_target": 1,
            "current_staff": "코너 (S급, 휴직중), 시에나 (도전중)",
            "main_tool": "Flow (Hailou AI Video), Flora AI, GPTs",
            "efficiency_improvement": "97%",
            "success_metric": "인스타 2,132만 조회수 + 블로그 키워드 모니터링 완료",
            "monthly_cost": "₩248,549",
            "roi": "2,797% (Flow), 개선중 (시에나 프로젝트)",
            "next_goal": "코너 복귀 후 시에나 멘토링, Flow 바이럴 파이프라인 구축",
            "s_grade_roadmap": "코너: 완료 / 시에나: AI 도구 숙련도 향상 필요"
        },
        {
            "department": "경영기획본부",
            "s_grade_count": 0,
            "s_grade_target": 1,
            "current_staff": "호, 헤스티",
            "main_tool": "Genspark AI",
            "efficiency_improvement": "75%",
            "success_metric": "PPT 제작시간 8h→2h, 비용 40만원 절감",
            "monthly_cost": "₩78,032",
            "roi": "500%",
            "next_goal": "전사 PPT 자동화 시스템 구축",
            "s_grade_roadmap": "경영 전략 수립 + AI 자동화 시스템 설계"
        },
        {
            "department": "커머스/개발",
            "s_grade_count": 0,
            "s_grade_target": 2,
            "current_staff": "테드, 웨인",
            "main_tool": "Cursor AI + Claude",
            "efficiency_improvement": "200%",
            "success_metric": "비개발자 MVP 개발, VBA 자동화",
            "monthly_cost": "₩104,658",
            "roi": "300%",
            "next_goal": "AI 코딩 전문가 양성, TM 시스템 고도화",
            "s_grade_roadmap": "복잡한 시스템 설계 + AI 개발 도구 마스터"
        },
        {
            "department": "스포츠플랫폼",
            "s_grade_count": 0,
            "s_grade_target": 1,
            "current_staff": "엘리스, 클로이",
            "main_tool": "UX 라이팅 챗봇, Flow",
            "efficiency_improvement": "50%",
            "success_metric": "카피 제작 1h→30m, AI 영상 삽입",
            "monthly_cost": "₩25,000",
            "roi": "150%",
            "next_goal": "스포츠 콘텐츠 특화 AI 시스템",
            "s_grade_roadmap": "스포츠 도메인 전문성 + 콘텐츠 자동화"
        },
        {
            "department": "컨택세일즈팀",
            "s_grade_count": 0,
            "s_grade_target": 1,
            "current_staff": "카밀라, 에이미",
            "main_tool": "TM AI 피드백 시스템",
            "efficiency_improvement": "파일럿 중",
            "success_metric": "상담시간 인당 30분 절감 (목표)",
            "monthly_cost": "₩15,000",
            "roi": "예상 400%",
            "next_goal": "AI 영업 코칭 시스템 완성",
            "s_grade_roadmap": "고객 심리 분석 + AI 피드백 시스템 운영"
        },
        {
            "department": "자금팀",
            "s_grade_count": 0,
            "s_grade_target": 1,
            "current_staff": "써니",
            "main_tool": "런웨이 분석 챗봇",
            "efficiency_improvement": "파일럿 중",
            "success_metric": "월별 분석 2h→10m (목표)",
            "monthly_cost": "₩10,000",
            "roi": "예상 300%",
            "next_goal": "재무 분석 자동화 시스템",
            "s_grade_roadmap": "재무 전략 수립 + AI 분석 도구 활용"
        },
        {
            "department": "야핏커머스",
            "s_grade_count": 0,
            "s_grade_target": 1,
            "current_staff": "벨, 지나, 헤이디",
            "main_tool": "Midjourney, 리드 자동화",
            "efficiency_improvement": "20%",
            "success_metric": "광고 이미지 비용 20만원 절감",
            "monthly_cost": "₩36,908",
            "roi": "100%",
            "next_goal": "프롬프트 교육 후 활용률 30% 달성",
            "s_grade_roadmap": "커머스 마케팅 전략 + AI 이미지 생성 마스터"
        }
    ],
    "evaluation_system": {
        "criteria": [
            "업무 핵심도 (KPI 직접기여)",
            "부서 적극성 (현업 참여/도입속도)",
            "개발 난이도 (낮을수록 가점)"
        ],
        "formula": "점수 = (핵심도 50%) + (적극성 30%) + (1/난이도 20%)",
        "grades": {
            "S": "≥85점, 즉시 확대 배포, 예산/인력 우선",
            "A": "70~84점, 즉시 확대 배포, 예산/인력 우선", 
            "B": "55~69점, 2주 내 개선→승격 또는 보류",
            "C": "40~54점, 파일럿만 유지, 4주 후 종료 판단",
            "D": "<40점, 즉시 중단, 학습 노트만 축적"
        }
    },
    "tasks": [
        {
            "no": 1,
            "department": "경영기획본부",
            "start_date": "6월 2주차",
            "manager": "호",
            "task": "계정별 원장 질문 챗봇",
            "tools": "openAI api, n8n, spread sheet",
            "status": "완료(중단)",
            "dept_performance": "월간 보고 파일 검색시간 3→1분",
            "company_impact": "리더 보고 용이",
            "dept_enthusiasm": "중",
            "dev_difficulty": "상",
            "task_importance": "중",
            "dept_level": "중",
            "improvement": "숫자 데이터 정확도 미흡으로 신뢰성 부족, 업무 영향도 낮아 프로젝트 중단 결정"
        },
        {
            "no": 2,
            "department": "경영기획본부",
            "start_date": "7월 3주차",
            "manager": "호, 헤스티",
            "task": "월별 야나두 KPI PPT 제작",
            "tools": "genspark",
            "status": "완료",
            "dept_performance": "ppt 제작 8h→2h, 비용 40만원 절감",
            "company_impact": "리더 보고 용이",
            "dept_enthusiasm": "중",
            "dev_difficulty": "하",
            "task_importance": "하",
            "dept_level": "중",
            "improvement": "Genspark 프롬프트로 PPT 자동생성 활용"
        }
    ],
    "tool_performance": {
        "total_tools": 32,
        "active_tools": 17,
        "terminated_tools": 15,
        "july_cost": "₩1,158,195",
        "august_estimated": "₩623,609",
        "cost_reduction": "46.2%",
        "saved_amount": "₩534,586"
    },
    "top_tools": [
        {
            "name": "Flow (Hailou AI Video)",
            "status": "최고 효율",
            "monthly_cost": "₩248,549",
            "achievement": "9개 영상 → 인스타 2,132만 조회수 + 8만 팔로워",
            "roi": "2,797%",
            "cost_replacement": "₩720만 (기존 제작비 대비)",
            "recommendation": "법인카드 전환 + 월 30개 제작 확대"
        },
        {
            "name": "Cursor AI + Claude",
            "status": "핵심 도구",
            "monthly_cost": "₩104,658",
            "achievement": "비개발자 MVP 개발 (TM, 블로그, 단어장)",
            "roi": "300%",
            "cost_replacement": "개발 외주비 절감",
            "recommendation": "지속 사용 권장"
        },
        {
            "name": "Genspark AI",
            "status": "관찰 중",
            "monthly_cost": "₩78,032",
            "achievement": "PPT 제작 8h→2h, 비용 40만원 절감",
            "roi": "500%",
            "cost_replacement": "시간 98% 절감 (12h→15m)",
            "recommendation": "3개월 관찰 후 재평가"
        },
        {
            "name": "Midjourney",
            "status": "개선 필요",
            "monthly_cost": "₩36,908",
            "achievement": "활용률 5% (200개 중 10개 사용)",
            "roi": "100%",
            "cost_replacement": "실사용 비용 ₩3,690/장",
            "recommendation": "프롬프트 교육 후 활용률 30% 목표"
        }
    ],
    "terminated_tools": [
        {
            "name": "HeyGen + ElevenLabs",
            "reason": "AI 오드리 프로젝트 종료",
            "monthly_savings": "₩257,678",
            "previous_output": "36개/월 AI 뉴스, YouTube 16.8만 조회"
        },
        {
            "name": "Rork",
            "reason": "앱 빌드 테스트 완료",
            "monthly_savings": "₩68,972",
            "previous_output": "MVP 테스트 완료"
        }
    ],
    "sienna_projects": [
        {
            "month": "6월 1주차",
            "project": "SA 광고 소재 기반 썸네일 AI 제작",
            "tool": "Flora AI",
            "status": "중단",
            "goal": "자사 제품(책, 강의화면) 기반 AI 이미지 제작으로 시간 단축",
            "achievement": "광고소재 이미지 제작 필요성 감소",
            "efficiency_score": "하",
            "value_creation_score": "중",
            "capability_score": "중", 
            "optimization_score": "하",
            "challenge": "툴 어려움으로 시도 방법 제한적"
        },
        {
            "month": "6월 4주차",
            "project": "스르르 영단어 채널 콘텐츠 제작 챗봇",
            "tool": "GPTs, Perplexity, OpenAI API",
            "status": "중단",
            "goal": "어원,어근 중심 챗봇으로 AI 콘텐츠 생성 자동화",
            "achievement": "콘텐츠 제작 시간 단축 가능성 확인",
            "efficiency_score": "중",
            "value_creation_score": "중",
            "capability_score": "하",
            "optimization_score": "하",
            "challenge": "데이터 구축 및 중복 제거 부담"
        },
        {
            "month": "7월 4주차",
            "project": "블로그 '키워드' 검색 모니터링",
            "tool": "Claude, MCP, Cursor",
            "status": "완료",
            "goal": "AI 정리로 기존 정리시간 단축 및 리서치 시간 절약",
            "achievement": "시간 확보 및 부가가치 높은 업무 집중 가능",
            "efficiency_score": "하",
            "value_creation_score": "상",
            "capability_score": "중",
            "optimization_score": "하",
            "challenge": "Claude MCP 만족도 2.8/5점, 블로그 키워드 검색 웹 효용성 낮음"
        }
    ],
    "tiro_ai_usage": [
        {
            "department": "AI서포트팀",
            "manager": "디케이",
            "usage_minutes": 2355,
            "notes_count": 64,
            "rating": "⭐⭐⭐⭐⭐",
            "action": "유지"
        },
        {
            "department": "스포츠YC서비스",
            "manager": "유니스",
            "usage_minutes": 1358,
            "notes_count": 22,
            "rating": "⭐⭐⭐⭐⭐",
            "action": "유지"
        },
        {
            "department": "커머스사업",
            "manager": "에런",
            "usage_minutes": 1277,
            "notes_count": 33,
            "rating": "⭐⭐⭐⭐⭐",
            "action": "유지"
        },
        {
            "department": "경영지원본부",
            "manager": "호",
            "usage_minutes": 744,
            "notes_count": 9,
            "rating": "⭐⭐⭐⭐",
            "action": "유지"
        },
        {
            "department": "커머스개발",
            "manager": "테드",
            "usage_minutes": 409,
            "notes_count": 5,
            "rating": "⭐⭐⭐",
            "action": "유지"
        },
        {
            "department": "커머스사업부",
            "manager": "헤이디",
            "usage_minutes": 252,
            "notes_count": 8,
            "rating": "⭐⭐",
            "action": "플랜 다운그레이드"
        },
        {
            "department": "스포츠YC본부",
            "manager": "토미",
            "usage_minutes": 152,
            "notes_count": 6,
            "rating": "⭐⭐",
            "action": "플랜 다운그레이드"
        }
    ],
    "august_plans": [
        {
            "title": "S급 인재 양성 프로그램 론칭",
            "description": "Flow 성공사례를 모델로 각 부서별 AI 내재화 교육",
            "goals": ["부서별 1명씩 S급 후보 선정", "AI 내재화 4질문 체계 교육", "월간 성과 측정"],
            "schedule": "8/5 프로그램 설계, 8/12 부서별 교육, 8/26 1차 평가"
        },
        {
            "title": "Flow 바이럴 콘텐츠 자동화 파이프라인",
            "description": "코너 복귀 + 터지는 콘텐츠 자동 생성 시스템 구축",
            "goals": ["월 30개 영상 제작 체계", "바이럴 요소 자동 분석", "트렌드 반영 파이프라인"],
            "schedule": "8/5 트렌드 분석 시스템, 8/12 자동화 파이프라인, 8/19 대량 제작 테스트"
        },
        {
            "title": "TM 자동 피드백 시스템 (컨택세일즈)",
            "description": "콜 스크립트 기준표 마련, 정확도 QA & 할루시네이션 가드",
            "goals": ["상담시간 30분 절감", "성공율 향상", "AI 피드백 정확도 90%"],
            "schedule": "8/7 룰북, 8/19 파일럿, 8/30 확산"
        },
        {
            "title": "Midjourney 활용률 개선",
            "description": "프롬프트 스킬 교육 및 우수사례 공유",
            "goals": ["활용률 5% → 30%", "월 생성 쿼터 50개 제한", "우수 프롬프트 라이브러리"],
            "schedule": "8/8 교육 자료, 8/15 집중 교육, 8/29 성과 측정"
        }
    ],
    "ai_internalization": {
        "S": {
            "level": "시간단축 +압도적 성과",
            "design": "새로운 디자인 컨셉, 아트웍 스타일 제안 및 제작 프로세스 혁신 주도",
            "planning": "비즈니스 핵심 문제 해결 방안 및 선도적 전략 제안",
            "admin": "반복적인 행정 업무 자동화 및 결과 검증 시스템 설계/구축",
            "development": "구조적 개선 제안 및 주도 → AI 코드 분석/리뷰를 통해 아키텍처 개선, 잠재적 버그 사전 식별, 기술 부채 해결 등 선도적이고 구조적인 개선을 제안하고 주도"
        },
        "A": {
            "level": "시간단축 + 사람이한것과 동일한 성과",
            "design": "최종 사용 가능한 이미지/영상 소스 제작 및 후가공",
            "planning": "기획 논리 구조화 및 핵심 내용 정교화",
            "admin": "행정 법규의 논리 구조화 및 AI 기반 업무 프로세스 최적화",
            "development": "고급 문제 해결 및 최적화 → AI를 활용해 복잡한 알고리즘을 구현하거나, 레거시 코드를 리팩토링하고, 성능 최적화 방안을 도출하는 등 생산성을 극대화"
        },
        "B": {
            "level": "교육내용이행",
            "design": "디자인/영상 기획을 위한 레퍼런스, 시안, 스토리보드 초안 생성",
            "planning": "기획 리서치 및 아이디어 초안 생성",
            "admin": "주어진 가이드에 따라, 표준 행정 업무를 처리",
            "development": "일상적 개발 업무의 속도 향상 → IDE 내장 AI나 Copilot 등을 활용해 단순 함수/로직, 테스트 코드, 주석 등의 초안을 생성하여 개발 속도 향상"
        },
        "C": {
            "level": "결과물 도출어려움",
            "design": "의도와 맞지 않거나, 완성도가 현저히 떨어지는(e.g., 어색한 표현) 결과물 생성",
            "planning": "기획 의도와 무관하거나 완성도 낮은 결과물 생성",
            "admin": "결과물의 정확도가 낮아, 검토 및 재작업이 필수적",
            "development": "결과물 오류로 인한 재작업 유발 → AI가 생성한 코드의 오류나 컨텍스트를 파악하지 못하고 그대로 사용하여, 버그를 유발하거나 재작업"
        },
        "D": {
            "level": "태도문제 및 리소스낭비",
            "design": "태도 문제 및 리소스 낭비",
            "planning": "태도 문제 및 리소스 낭비",
            "admin": "태도 문제 및 리소스 낭비",
            "development": "활용 거부 또는 보안 위험 유발 → AI 활용을 거부하거나, 보안 규정을 위반하며 코드를 유출/사용하여 리소스 낭비 및 위험 유발"
        }
    },
    "risks": [
        {
            "title": "데이터 정확도",
            "description": "숫자 오류 발생(원장 챗봇 사례)",
            "solution": "검증 레이어/샘플링 필수, 임계치 미달 시 자동 중단"
        },
        {
            "title": "참여 저조",
            "description": "평가체계 미비",
            "solution": "S/A 보상, C/D 중단 원칙 공지"
        },
        {
            "title": "모델 할루시네이션",
            "description": "TM 피드백 정확도 저하",
            "solution": "룰베이스 + 근거출처 표기 병행"
        }
    ]
}

def load_ceo_data():
    """CEO 브리핑 데이터 로드"""
    if os.path.exists(CEO_DATA_FILE):
        try:
            with open(CEO_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CEO_DATA.copy()
    return DEFAULT_CEO_DATA.copy()

def save_ceo_data(data):
    """CEO 브리핑 데이터 저장"""
    try:
        with open(CEO_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

@app.route('/')
def ceo_dashboard():
    """CEO 대시보드 페이지"""
    data = load_ceo_data()
    return render_template('ceo_dashboard.html', data=data)

@app.route('/admin')
def ceo_admin():
    """CEO 브리핑 관리자 페이지"""
    data = load_ceo_data()
    return render_template('ceo_admin.html', data=data)

@app.route('/admin/update', methods=['POST'])
def update_ceo_data():
    """CEO 브리핑 데이터 업데이트"""
    try:
        data = load_ceo_data()
        
        # Header 업데이트
        if 'header_title' in request.form:
            data['header']['title'] = request.form['header_title']
        if 'header_subtitle' in request.form:
            data['header']['subtitle'] = request.form['header_subtitle']
        
        # KPIs 업데이트
        if 'task_completed' in request.form:
            data['kpis']['task_status']['completed'] = int(request.form['task_completed'])
        if 'task_in_progress' in request.form:
            data['kpis']['task_status']['in_progress'] = int(request.form['task_in_progress'])
        if 'task_not_started' in request.form:
            data['kpis']['task_status']['not_started'] = int(request.form['task_not_started'])
        if 'task_stopped' in request.form:
            data['kpis']['task_status']['stopped'] = int(request.form['task_stopped'])
        
        # 과제 상태 값 업데이트
        total_tasks = (data['kpis']['task_status']['completed'] + 
                      data['kpis']['task_status']['in_progress'] + 
                      data['kpis']['task_status']['not_started'] + 
                      data['kpis']['task_status']['stopped'])
        
        data['kpis']['task_status']['value'] = f"완료 {data['kpis']['task_status']['completed']} · 진행 {data['kpis']['task_status']['in_progress']} · 시작전 {data['kpis']['task_status']['not_started']} · 중단 {data['kpis']['task_status']['stopped']}"
        data['kpis']['task_status']['detail'] = f"총 {total_tasks}개 과제"
        
        # Core Impact 업데이트
        if 'core_time_saved' in request.form:
            data['kpis']['core_impact']['time_saved'] = int(request.form['core_time_saved'])
            data['kpis']['core_impact']['value'] = f"PPT 제작 {data['kpis']['core_impact']['time_saved']}h 절감/월"
        
        if 'core_cost_saved' in request.form:
            data['kpis']['core_impact']['cost_saved'] = int(request.form['core_cost_saved'])
            data['kpis']['core_impact']['detail'] = f"+ 비용 {data['kpis']['core_impact']['cost_saved']/10000:.0f}만원 절감 (KPI 리포트)"
        
        # Field Efficiency 업데이트
        if 'field_time_saved' in request.form:
            data['kpis']['field_efficiency']['time_saved_per_person'] = int(request.form['field_time_saved'])
            data['kpis']['field_efficiency']['value'] = f"TM 상담 {data['kpis']['field_efficiency']['time_saved_per_person']}분/인 절감"
        
        # Objectives 업데이트
        if 'obj_why' in request.form:
            data['objectives']['why'] = request.form['obj_why']
        if 'obj_what' in request.form:
            data['objectives']['what'] = request.form['obj_what']
        if 'obj_how' in request.form:
            data['objectives']['how'] = request.form['obj_how']
        
        if save_ceo_data(data):
            flash('데이터가 성공적으로 업데이트되었습니다.', 'success')
        else:
            flash('데이터 저장 중 오류가 발생했습니다.', 'error')
            
    except Exception as e:
        flash(f'업데이트 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('ceo_admin'))

@app.route('/admin/reset')
def reset_ceo_data():
    """CEO 브리핑 데이터 리셋"""
    if save_ceo_data(DEFAULT_CEO_DATA.copy()):
        flash('데이터가 기본값으로 리셋되었습니다.', 'success')
    else:
        flash('리셋 중 오류가 발생했습니다.', 'error')
    return redirect(url_for('ceo_admin'))

@app.route('/api/chart-data')
def get_chart_data():
    """차트 데이터 API - 과제 현황 및 성과 중심"""
    data = load_ceo_data()
    
    # 7월 과제 현황 (도넛 차트)
    task_status = {
        'labels': ['완료', '진행중', '시작전', '중단'],
        'data': [4, 5, 2, 1],
        'colors': ['#059669', '#3b82f6', '#f59e0b', '#dc2626']
    }
    
    # 부서별 과제 분포 (바 차트)
    dept_tasks = {
        'labels': ['마케팅팀', '커머스/개발', '경영기획본부', '기타부서'],
        'data': [4, 3, 2, 3],
        'colors': ['#8b5cf6', '#3b82f6', '#10b981', '#6b7280']
    }
    
    # 비용 절감 현황 (파이 차트)
    cost_savings = {
        'labels': ['KPI PPT 자동화', 'AI 이미지 적용', 'VBA 모듈화', '기타'],
        'data': [40, 20, 15, 10],  # 만원 단위
        'colors': ['#10b981', '#3b82f6', '#f59e0b', '#6b7280']
    }
    
    # 시간 절감 현황 (바 차트)
    time_savings = {
        'labels': ['KPI PPT', 'UX 라이팅', 'TM 상담', '광고 제작'],
        'data': [6, 0.5, 30, 2],  # 시간 단위
        'colors': ['#10b981', '#8b5cf6', '#3b82f6', '#f59e0b']
    }
    
    # S급 인재 현황 차트
    s_grade_progress = {
        'labels': ['현재 S급', '목표까지 필요'],
        'data': [
            data['kpis']['s_grade_talent']['current'],
            data['kpis']['s_grade_talent']['target'] - data['kpis']['s_grade_talent']['current']
        ],
        'colors': ['#8b5cf6', '#e5e7eb']
    }
    
    # Flow 성과 분석
    flow_metrics = {
        'labels': ['조회수 (백만)', 'ROI (%)', '팔로워 증가 (만)', '비용절감 (백만원)'],
        'data': [
            data['kpis']['flow_success']['views'] / 1000000,  # 2132만 -> 21.32
            data['kpis']['flow_success']['roi'] / 10,  # 2797% -> 279.7 (스케일 조정)
            data['kpis']['flow_success']['followers'] / 10000,  # 8만 -> 8
            7.2  # 720만원 -> 7.2
        ],
        'colors': ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    }
    
    return jsonify({
        'task_status': task_status,
        'dept_tasks': dept_tasks,
        'cost_savings': cost_savings,
        'time_savings': time_savings,
        's_grade_progress': s_grade_progress,
        'flow_metrics': flow_metrics
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8081))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port) 