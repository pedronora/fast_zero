from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='dunossauro', email='duno@ssauro.com', password='senha123'
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'duno@ssauro.com')
    )

    assert result.id == 1
    assert result.username == 'dunossauro'
