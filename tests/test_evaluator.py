"""
Tests for Evaluator Agent
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from agents.evaluator import EvaluatorAgent
from utils.helpers import setup_logging


@pytest.fixture
def config():
    """Test configuration"""
    return {
        'openai_model': 'gpt-4',
        'confidence_min': 0.6,
        'temperature': 0.3
    }


@pytest.fixture
def logger(config):
    """Test logger"""
    return setup_logging(config)


@pytest.fixture
def evaluator(config, logger):
    """Evaluator agent instance"""
    return EvaluatorAgent(config, logger)


@pytest.fixture
def sample_hypothesis():
    """Sample hypothesis for testing"""
    return {
        'hypothesis': 'ROAS declined 15% due to creative fatigue',
        'reasoning': 'CTR dropped while spend remained constant',
        'data_evidence': 'ROAS: 4.2 vs 4.9, CTR: 1.2% vs 1.6%',
        'category': 'creative_decay'
    }


@pytest.fixture
def sample_data_summary():
    """Sample data summary"""
    return {
        'overview': {
            'total_spend': 50000,
            'total_revenue': 200000,
            'overall_roas': 4.0
        },
        'time_series': {
            'last_7_days': {'roas': 4.2, 'ctr': 0.012},
            'prev_7_days': {'roas': 4.9, 'ctr': 0.016},
            'change': {'roas_change': -0.7, 'roas_change_pct': -14.3}
        }
    }


def test_evaluator_initialization(evaluator):
    """Test evaluator initializes correctly"""
    assert evaluator is not None
    assert evaluator.config['confidence_min'] == 0.6


def test_evaluation_structure(evaluator, sample_hypothesis, sample_data_summary):
    """Test evaluation returns proper structure"""
    result = evaluator.evaluate(sample_hypothesis, sample_data_summary)
    
    assert 'hypothesis' in result
    assert 'confidence' in result
    assert 'evidence' in result
    assert 'reasoning' in result
    
    assert isinstance(result['confidence'], (int, float))
    assert 0 <= result['confidence'] <= 1


def test_confidence_scoring(evaluator, sample_hypothesis, sample_data_summary):
    """Test confidence score is within valid range"""
    result = evaluator.evaluate(sample_hypothesis, sample_data_summary)
    
    confidence = result['confidence']
    assert 0.0 <= confidence <= 1.0


def test_low_confidence_detection(config, logger):
    """Test detection of low-confidence hypotheses"""
    evaluator = EvaluatorAgent(config, logger)
    
    weak_hypothesis = {
        'hypothesis': 'Performance changed because of unknown factors',
        'reasoning': 'Things just changed',
        'data_evidence': 'Some numbers went up and down',
        'category': 'other'
    }
    
    result = evaluator.evaluate(weak_hypothesis, {'overview': {}})
    
    # Weak hypothesis should have lower confidence
    assert result['confidence'] < 0.7


def test_batch_evaluation(evaluator, sample_data_summary):
    """Test evaluating multiple hypotheses"""
    hypotheses = [
        {
            'hypothesis': 'Hypothesis 1',
            'reasoning': 'Reason 1',
            'data_evidence': 'Evidence 1',
            'category': 'creative_decay'
        },
        {
            'hypothesis': 'Hypothesis 2',
            'reasoning': 'Reason 2',
            'data_evidence': 'Evidence 2',
            'category': 'audience_fatigue'
        }
    ]
    
    results = evaluator.batch_evaluate(hypotheses, sample_data_summary)
    
    assert len(results) == 2
    assert all('confidence' in r for r in results)


def test_evaluation_includes_metrics(evaluator, sample_hypothesis, sample_data_summary):
    """Test evaluation includes quantitative metrics"""
    result = evaluator.evaluate(sample_hypothesis, sample_data_summary)
    
    # Should have some form of metrics or evidence with numbers
    assert result['evidence'] or result.get('metrics')


def test_recommendation_generation(evaluator, sample_hypothesis, sample_data_summary):
    """Test evaluator provides recommendations"""
    result = evaluator.evaluate(sample_hypothesis, sample_data_summary)
    
    assert 'recommendation' in result
    assert len(result['recommendation']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])