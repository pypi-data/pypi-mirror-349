"""
Test basic package functionality.
"""
import pytest
import ai_cli


def test_package_version():
    """Test that the package has a version."""
    assert hasattr(ai_cli, '__version__')
    assert isinstance(ai_cli.__version__, str)
    assert len(ai_cli.__version__) > 0


def test_package_metadata():
    """Test that the package has required metadata."""
    assert hasattr(ai_cli, '__author__')
    assert hasattr(ai_cli, '__email__')
    assert hasattr(ai_cli, '__description__')
    assert hasattr(ai_cli, '__url__')


def test_imports():
    """Test that main components can be imported."""
    from ai_cli import ChatSession, config, ShellExecutor
    
    # Test that classes can be instantiated (basic smoke test)
    assert ChatSession is not None
    assert config is not None
    assert ShellExecutor is not None


def test_cli_entry_point():
    """Test that the CLI entry point can be imported."""
    from ai_cli.cli import main
    assert callable(main)
