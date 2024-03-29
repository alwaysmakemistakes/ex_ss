"""Initial migration

Revision ID: 590f8ec14648
Revises: 
Create Date: 2023-06-25 20:12:05.495450

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

# revision identifiers, used by Alembic.
revision = '590f8ec14648'
down_revision = None
branch_labels = None
depends_on = None

def cata_upg():
    """Add any optional data upgrade migrations here!"""

    table = sa.sql.table('categories', sa.sql.column('name', sa.String))

    op.bulk_insert(table,
        [
            {'name': 'Роман-эпопея'},
            {'name': 'Роман'},
            {'name': 'Повесть'},
            {'name': 'Новелла'},
            {'name': 'Притча'},
            {'name': 'Сказка'},
            {'name': 'Послание'},
            {'name': 'Драма'},
            {'name': 'Комедия'},
            {'name': 'Трагедия'},
            {'name': 'Баллада'},
            {'name': 'Поэма'},
        ]
    )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_categories')),
    sa.UniqueConstraint('name', name=op.f('uq_categories_name'))
    )
    op.create_table('images',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('file_name', sa.String(length=100), nullable=False),
    sa.Column('mime_type', sa.String(length=100), nullable=False),
    sa.Column('md5_hash', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_images')),
    sa.UniqueConstraint('md5_hash', name=op.f('uq_images_md5_hash'))
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_name', sa.Text(), nullable=False),
    sa.Column('role_description', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles'))
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('publisher', sa.String(length=100), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('volume', sa.Integer(), nullable=False),
    sa.Column('rating_sum', sa.Integer(), nullable=False),
    sa.Column('rating_num', sa.Integer(), nullable=False),
    sa.Column('id_image', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['id_image'], ['images.id'], name=op.f('fk_books_id_image_images'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_books'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('middle_name', sa.String(length=100), nullable=True),
    sa.Column('login', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=200), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_users_role_id_roles')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('login', name=op.f('uq_users_login'))
    )
    op.create_table('book_category',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name=op.f('fk_book_category_book_id_books'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], name=op.f('fk_book_category_category_id_categories'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('book_id', 'category_id', name=op.f('pk_book_category'))
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name=op.f('fk_reviews_book_id_books'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_reviews_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_reviews'))
    )
    role_up()
    us_up()
    cata_upg()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('book_category')
    op.drop_table('users')
    op.drop_table('books')
    op.drop_table('roles')
    op.drop_table('images')
    op.drop_table('categories')
    # ### end Alembic commands ###

def role_up():
    """Add any optional data upgrade migrations here!"""
    table = sa.sql.table('roles', sa.sql.column('role_name', sa.String), sa.sql.column('role_description', sa.String))
    op.bulk_insert(table,
        [
            {'role_name': 'Администратор', 'role_description': 'Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг.'},
            {'role_name': 'Модератор', 'role_description': 'Может редактировать данные книг и производить модерацию рецензий.'},
            {'role_name': 'Пользователь', 'role_description': 'Может оставлять рецензии.'},
        ]
    )

from werkzeug.security import generate_password_hash
def us_up():

    table = sa.sql.table('users', sa.sql.column('login', sa.String), sa.sql.column('password_hash', sa.String),sa.sql.column('last_name', sa.String),
        sa.sql.column('first_name', sa.String), sa.sql.column('middle_name', sa.String))
    op.bulk_insert(table,
        [
            {'login': 'vital1', 'password_hash': generate_password_hash('qwerty'), 'last_name': 'Виталио1', 'first_name': 'Витал', 'middle_name': 'Виталыч1', 'role_id': 1},
            {'login': 'vital2', 'password_hash': generate_password_hash('qwerty'), 'last_name': 'Виталио2', 'first_name': 'Витал', 'middle_name': 'Виталыч2', 'role_id': 2},
            {'login': 'vital3', 'password_hash': generate_password_hash('qwerty'), 'last_name': 'Виталио3', 'first_name': 'Витал', 'middle_name': 'Виталыч3', 'role_id': 3},
        ]
    )
