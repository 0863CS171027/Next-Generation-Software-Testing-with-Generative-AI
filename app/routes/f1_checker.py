"""
Routes for F1-Score metrics API
Provides endpoints for F1-score calculation and test evaluation
"""

from flask import Blueprint, jsonify, request
from f1_checker import F1ScoreChecker
from datetime import datetime

f1_checker_bp = Blueprint('f1_checker', __name__, url_prefix='/f1-checker')
checker = F1ScoreChecker()


@f1_checker_bp.route('/calculate', methods=['POST'])
def calculate_f1():
    """Calculate F1-score from confusion matrix"""
    try:
        data = request.get_json()
        
        tp = data.get('tp', 0)
        fp = data.get('fp', 0)
        fn = data.get('fn', 0)
        tn = data.get('tn', 0)
        
        f1_score = checker.calculate_f1_score(tp, fp, fn, tn)
        
        return jsonify({
            'status': 'success',
            'f1_score': f1_score,
            'grade': checker.get_f1_grade(f1_score)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@f1_checker_bp.route('/evaluate', methods=['POST'])
def evaluate_tests():
    """Evaluate test effectiveness"""
    try:
        data = request.get_json()
        
        metrics = checker.evaluate_test_effectiveness(data)
        assessment = checker.assess_quality(metrics)
        
        return jsonify({
            'status': 'success',
            'metrics': metrics,
            'assessment': assessment
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@f1_checker_bp.route('/analyze-defects', methods=['POST'])
def analyze_defects():
    """Analyze defect detection"""
    try:
        data = request.get_json()
        
        analysis = checker.analyze_defect_detection(data)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@f1_checker_bp.route('/batch-evaluate', methods=['POST'])
def batch_evaluate():
    """Batch evaluate multiple projects"""
    try:
        data = request.get_json()
        projects = data.get('projects', [])
        
        results = checker.batch_evaluate(projects)
        
        return jsonify({
            'status': 'success',
            'results': results,
            'count': len(results)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@f1_checker_bp.route('/history', methods=['GET'])
def get_history():
    """Get evaluation history"""
    try:
        return jsonify({
            'status': 'success',
            'history': checker.history,
            'count': len(checker.history)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@f1_checker_bp.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'module': 'f1_checker',
        'timestamp': datetime.utcnow().isoformat()
    }), 200
