"""
REST API routes for programmatic access
"""

from flask import Blueprint, jsonify, request
from app.models import db, SprintReport, GeneratedTest, TestRequirement
from sqlalchemy import func

api_bp = Blueprint('api', __name__)


@api_bp.route('/v1/status', methods=['GET'])
def api_status():
    """API status endpoint"""
    return jsonify({
        'api_version': '1.0',
        'status': 'active',
        'service': 'Next-Generation Software Testing with Generative AI'
    }), 200


@api_bp.route('/v1/sprints/stats', methods=['GET'])
def sprint_stats():
    """Get sprint statistics"""
    try:
        total = db.session.query(SprintReport).count()
        
        stats = {
            'total_sprints': total,
            'avg_coverage': round(db.session.query(
                func.avg(SprintReport.coverage_pct)
            ).scalar() or 0.0, 2),
            'total_tests_generated': db.session.query(
                func.sum(SprintReport.generated_count)
            ).scalar() or 0,
            'total_tests_executed': db.session.query(
                func.sum(SprintReport.executed_count)
            ).scalar() or 0,
            'total_defects_found': db.session.query(
                func.sum(SprintReport.defect_count)
            ).scalar() or 0,
            'total_tests_healed': db.session.query(
                func.sum(SprintReport.healed_count)
            ).scalar() or 0
        }
        
        return jsonify(stats), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/v1/requirements', methods=['GET'])
def get_requirements():
    """Get all requirements"""
    try:
        requirements = TestRequirement.query.all()
        
        return jsonify({
            'total': len(requirements),
            'requirements': [
                {
                    'id': req.req_id,
                    'name': req.name,
                    'description': req.description,
                    'risk_score': req.risk_score
                }
                for req in requirements
            ]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/v1/requirements', methods=['POST'])
def create_requirement():
    """Create a new requirement"""
    try:
        data = request.get_json()
        
        req = TestRequirement(
            req_id=data.get('req_id'),
            name=data.get('name'),
            description=data.get('description'),
            signature=data.get('signature'),
            module=data.get('module'),
            risk_score=data.get('risk_score', 0.5)
        )
        
        db.session.add(req)
        db.session.commit()
        
        return jsonify({
            'id': req.req_id,
            'name': req.name
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/v1/health', methods=['GET'])
def health_check():
    """Health check for API"""
    try:
        # Try to query the database
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503
