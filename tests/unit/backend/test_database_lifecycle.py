from unittest.mock import MagicMock, patch

from app.api.deps import get_db


def test_get_db_lifecycle():
    with patch("app.api.deps.SessionLocal") as mock_session_local:
        mock_db = MagicMock()
        mock_session_local.return_value = mock_db
        
        gen = get_db()
        db = next(gen)
        assert db == mock_db
        
        # Closing generator triggers cleanup
        try:
            next(gen)
        except StopIteration:
            pass
            
        mock_db.close.assert_called_once()
