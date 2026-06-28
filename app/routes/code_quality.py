"""
Code Quality Assessment Module - REST API Routes
Provides intelligent code analysis, quality metrics, and assessment insights
"""

from flask import Blueprint, jsonify, request
from app.models import db, CodeQualityMetric
from datetime import datetime
import json

code_quality_bp = Blueprint('code_quality', __name__, url_prefix='/code-quality')


@code_quality_bp.route('/analyze', methods=['GET'])
def analyze_code_quality():
    """Analyze code quality metrics"""
    project = request.args.get('project', None)
    metric_type = request.args.get('type', 'general')
    
    try:
        metrics = CodeQualityMetric.query.all()
        
        if project:
            metrics = [m for m in metrics if m.project == project]
        
        return jsonify({
            'status': 'success',
            'metrics': [
                {
                    'id': m.id,
                    'project': m.project,
                    'type': m.metric_type,
                    'value': m.value,
                    'threshold': m.threshold,
                    'status': m.status,
                    'assessed_at': m.assessed_at.isoformat()
                }
                for m in metrics
            ]
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@code_quality_bp.route('/metrics/all', methods=['GET'])
def get_all_metrics():
    """Get all code quality metrics"""
    try:
        metrics = CodeQualityMetric.query.all()
        
        summary = {
            'total_metrics': len(metrics),
            'by_type': {},
            'metrics': []
        }
        
        for metric in metrics:
            if metric.metric_type not in summary['by_type']:
                summary['by_type'][metric.metric_type] = 0
            summary['by_type'][metric.metric_type] += 1
            
            summary['metrics'].append({
                'id': metric.id,
                'project': metric.project,
                'metric_type': metric.metric_type,
                'value': metric.value,
                'threshold': metric.threshold,
                'status': metric.status
            })
        
        return jsonify({
            'status': 'success',
            'summary': summary
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@code_quality_bp.route('/assessment/<string:project_id>', methods=['GET'])
def get_project_assessment(project_id):
    """Get comprehensive code quality assessment for a project"""
    try:
        metrics = CodeQualityMetric.query.filter_by(project=project_id).all()
        
        if not metrics:
            return jsonify({
                'status': 'error',
                'message': 'Project not found'
            }), 404
        
        # Calculate overall score
        total_score = 0
        weighted_count = 0
        
        assessment = {
            'project_id': project_id,
            'total_metrics': len(metrics),
            'metrics': [],
            'status': 'evaluated',
            'assessed_at': datetime.utcnow().isoformat()
        }
        
        for metric in metrics:
            metric_data = {
                'name': metric.metric_type,
                'value': metric.value,
                'threshold': metric.threshold,
                'status': metric.status,
                'score': calculate_score(metric.value, metric.threshold)
            }
            assessment['metrics'].append(metric_data)
            total_score += metric_data['score']
            weighted_count += 1
        
        if weighted_count > 0:
            overall_score = total_score / weighted_count
            assessment['overall_score'] = round(overall_score, 2)
            assessment['grade'] = get_quality_grade(overall_score)
        
        return jsonify({
            'status': 'success',
            'assessment': assessment
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@code_quality_bp.route('/metrics', methods=['POST'])
def add_metric():
    """Add new code quality metric"""
    try:
        data = request.get_json()
        
        metric = CodeQualityMetric(
            project=data.get('project'),
            metric_type=data.get('metric_type'),
            value=data.get('value'),
            threshold=data.get('threshold'),
            status=data.get('status', 'pending'),
            assessment_data=data.get('assessment_data')
        )
        
        db.session.add(metric)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'metric_id': metric.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@code_quality_bp.route('/report', methods=['GET'])
def generate_report():
    """Generate comprehensive quality report"""
    try:
        metrics = CodeQualityMetric.query.all()
        
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'total_evaluations': len(metrics),
            'metrics_by_status': {
                'pass': len([m for m in metrics if m.status == 'pass']),
                'fail': len([m for m in metrics if m.status == 'fail']),
                'warning': len([m for m in metrics if m.status == 'warning'])
            },
            'projects': {}
        }
        
        for metric in metrics:
            if metric.project not in report['projects']:
                report['projects'][metric.project] = {
                    'metrics_count': 0,
                    'metrics': []
                }
            
            report['projects'][metric.project]['metrics_count'] += 1
            report['projects'][metric.project]['metrics'].append({
                'type': metric.metric_type,
                'value': metric.value,
                'status': metric.status
            })
        
        return jsonify({
            'status': 'success',
            'report': report
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@code_quality_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for code quality module"""
    try:
        metric_count = CodeQualityMetric.query.count()
        
        return jsonify({
            'status': 'healthy',
            'module': 'code_quality_assessment',
            'metrics_in_database': metric_count
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


def calculate_score(value, threshold):
    """Calculate metric score"""
    if threshold == 0:
        return 5.0
    
    ratio = value / threshold
    if ratio >= 1.0:
        return 10.0
    elif ratio >= 0.9:
        return 9.0
    elif ratio >= 0.8:
        return 8.0
    elif ratio >= 0.7:
        return 7.0
    elif ratio >= 0.6:
        return 6.0
    else:
        return max(0, 5.0 * ratio)


def get_quality_grade(score):
    """Get quality grade based on score"""
    if score >= 9.0:
        return 'A+ (Excellent)'
    elif score >= 8.0:
        return 'A (Very Good)'
    elif score >= 7.0:
        return 'B (Good)'
    elif score >= 6.0:
        return 'C (Acceptable)'
    elif score >= 5.0:
        return 'D (Needs Improvement)'
    else:
        return 'F (Critical)'
