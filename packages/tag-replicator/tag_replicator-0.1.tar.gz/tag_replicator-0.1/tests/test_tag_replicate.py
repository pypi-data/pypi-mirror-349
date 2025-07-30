import pytest
from unittest.mock import patch, MagicMock
import tag_replicate

@pytest.fixture
def mock_tagger():
    mock = MagicMock()
    mock.get_tags.side_effect = lambda rid: {'Environment': 'dev'} if 'src' in rid else {'Environment': 'prod'}
    mock.apply_tags.return_value = None
    return mock

def test_clean_applies_exact_tags(monkeypatch, mock_tagger):
    monkeypatch.setattr('tag_replicate.get_tagger', lambda t: mock_tagger)
    monkeypatch.setattr('builtins.input', lambda _: 'yes')

    args = [
        'tag_replicate.py',
        '--type', 'ec2',
        '--model', 'src-id',
        '--target', 'tgt-id',
        '--clean'
    ]
    with patch.object(tag_replicate, 'sys') as mock_sys:
        mock_sys.argv = args
        tag_replicate.main()
        mock_tagger.apply_tags.assert_called_once_with('tgt-id', {'Environment': 'dev'}, True)

def test_preserve_existing_tags(monkeypatch, mock_tagger):
    monkeypatch.setattr('tag_replicate.get_tagger', lambda t: mock_tagger)
    monkeypatch.setattr('builtins.input', lambda _: 'yes')

    args = [
        'tag_replicate.py',
        '--type', 'ec2',
        '--model', 'src-id',
        '--target', 'tgt-id'
    ]
    with patch.object(tag_replicate, 'sys') as mock_sys:
        mock_sys.argv = args
        tag_replicate.main()
        expected_tags = {'Environment': 'dev'}
        mock_tagger.apply_tags.assert_called_once_with('tgt-id', expected_tags, False)
