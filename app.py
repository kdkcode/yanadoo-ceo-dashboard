from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 데이터 파일 경로
DATA_FILE = 'report_data.json'

# 기본 데이터 구조
DEFAULT_DATA = {
    "executive_summary": {
        "title": "AI 도구 종합 브리핑",
        "subtitle": "2024년 7-8월 투자 현황 및 성과 분석",
        "metrics": {
            "july_investment": {"value": "₩1,158,195", "desc": "32개 도구 운영"},
            "august_cost": {"value": "₩623,609", "desc": "-46.2% 절감"},
            "total_reach": {"value": "4,280만", "desc": "YouTube + 인스타"},
            "highest_roi": {"value": "+3,484%", "desc": "Flow 도구"}
        }
    },
    "cost_analysis": {
        "title": "💰 비용 구조 변화 및 최적화",
        "alert": {
            "title": "⚠️ 중요 발견사항",
            "content": "Flow 도구가 개인카드로 ₩248,549 결제되고 있음 (법인카드 전환 검토 필요)<br>7월 대비 8월 46.2% 비용 절감으로 연간 ₩6.4M 절약 예상"
        }
    },
    "top_tool": {
        "name": "Flow (Hailou AI Video)",
        "status": "최고 효율",
        "monthly_cost": "₩248,549",
        "content_count": "9개",
        "instagram_views": "2,132만",
        "follower_increase": "8만명",
        "roi": "+2,797%",
        "analysis": "단 9개 영상으로 2,132만 조회수와 8만 팔로워 증가 달성. 영상당 237만회 조회는 업계 최고 수준.<br>기존 영상 제작비(₩720만) 대비 96.5% 절감하며 ROI 2,797% 달성.<br><strong>권장사항:</strong> 월 30개로 제작 확대 시 연간 1억뷰 예상, 법인카드 전환 필요"
    },
    "tools": [
        {
            "name": "Cursor AI + Claude",
            "status": "핵심 도구",
            "monthly_cost": "₩104,658",
            "projects": "3개",
            "productivity": "+200%",
            "evaluation": "개발팀 필수 도구로 자리매김. TM 시스템 구축의 핵심이며 지속 사용 권장."
        },
        {
            "name": "HeyGen + ElevenLabs (AI 오드리)",
            "status": "8월 종료",
            "monthly_cost": "₩257,678",
            "content": "36개/월",
            "youtube_views": "16.8만",
            "evaluation": "프로젝트 방향 전환으로 8월 중 해지. 월 ₩257,678 절감 효과."
        },
        {
            "name": "Midjourney",
            "status": "개선 필요",
            "monthly_cost": "₩36,908",
            "utilization": "5%",
            "real_cost": "₩3,690/장",
            "evaluation": "프롬프트 스킬 교육 시급. 월 생성 쿼터 제한(50개) 및 우수사례 공유 필요."
        },
        {
            "name": "Genspark AI",
            "status": "관찰 중",
            "monthly_cost": "₩78,032",
            "frequency": "2-3회/월",
            "time_saving": "98%",
            "evaluation": "재무제표 등 전문 PPT 제작에 탁월. 3개월 추가 관찰 후 재평가."
        }
    ],
    "insights": {
        "priority": "1. Flow 법인카드 전환 및 제작 확대<br>2. AI 오드리 해지 완료 (₩257K 절감)<br>3. Midjourney 활용률 개선 교육",
        "cost_optimization": "8월 46.2% 비용 절감으로 연간 ₩6.4M 절약<br>Flow 도구 ROI 2,797% 달성<br>저활용 도구 정리로 효율성 증대",
        "growth_strategy": "Flow 제작량 월 30개로 확대<br>인스타그램 연간 1억뷰 목표<br>개발 도구 지속 투자로 생산성 유지",
        "risk_management": "개인카드 결제 도구 법인 전환<br>Midjourney 활용률 30% 미달 시 해지<br>신규 도구 도입 시 3개월 평가 기간"
    }
}

def load_data():
    """데이터 파일에서 데이터를 로드합니다."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()

def save_data(data):
    """데이터를 파일에 저장합니다."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

@app.route('/')
def index():
    """메인 보고서 페이지"""
    data = load_data()
    return render_template('report.html', data=data)

@app.route('/admin')
def admin():
    """관리자 페이지"""
    data = load_data()
    return render_template('admin.html', data=data)

@app.route('/admin/update', methods=['POST'])
def update_data():
    """데이터 업데이트"""
    try:
        data = load_data()
        
        # Executive Summary 업데이트
        if 'exec_title' in request.form:
            data['executive_summary']['title'] = request.form['exec_title']
        if 'exec_subtitle' in request.form:
            data['executive_summary']['subtitle'] = request.form['exec_subtitle']
        
        # Metrics 업데이트
        metrics = ['july_investment', 'august_cost', 'total_reach', 'highest_roi']
        for metric in metrics:
            if f'{metric}_value' in request.form:
                data['executive_summary']['metrics'][metric]['value'] = request.form[f'{metric}_value']
            if f'{metric}_desc' in request.form:
                data['executive_summary']['metrics'][metric]['desc'] = request.form[f'{metric}_desc']
        
        # Cost Analysis 업데이트
        if 'cost_title' in request.form:
            data['cost_analysis']['title'] = request.form['cost_title']
        if 'alert_title' in request.form:
            data['cost_analysis']['alert']['title'] = request.form['alert_title']
        if 'alert_content' in request.form:
            data['cost_analysis']['alert']['content'] = request.form['alert_content']
        
        # Top Tool 업데이트
        top_tool_fields = ['name', 'status', 'monthly_cost', 'content_count', 
                          'instagram_views', 'follower_increase', 'roi', 'analysis']
        for field in top_tool_fields:
            if f'top_tool_{field}' in request.form:
                data['top_tool'][field] = request.form[f'top_tool_{field}']
        
        # Tools 업데이트
        for i, tool in enumerate(data['tools']):
            for field in tool.keys():
                form_key = f'tool_{i}_{field}'
                if form_key in request.form:
                    data['tools'][i][field] = request.form[form_key]
        
        # Insights 업데이트
        insight_fields = ['priority', 'cost_optimization', 'growth_strategy', 'risk_management']
        for field in insight_fields:
            if f'insight_{field}' in request.form:
                data['insights'][field] = request.form[f'insight_{field}']
        
        if save_data(data):
            flash('데이터가 성공적으로 업데이트되었습니다.', 'success')
        else:
            flash('데이터 저장 중 오류가 발생했습니다.', 'error')
            
    except Exception as e:
        flash(f'업데이트 중 오류가 발생했습니다: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

@app.route('/admin/reset')
def reset_data():
    """데이터를 기본값으로 리셋"""
    if save_data(DEFAULT_DATA.copy()):
        flash('데이터가 기본값으로 리셋되었습니다.', 'success')
    else:
        flash('리셋 중 오류가 발생했습니다.', 'error')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 