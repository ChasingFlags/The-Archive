from models import User as UserModel, Notes as NotesModel, FlagTable as FlagModel, session, Token as TokenModel
import graphene
from graphene_sqlalchemy import (SQLAlchemyConnectionField, SQLAlchemyObjectType)
from extensions import bcrypt
from typing import Optional
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, jwt_required)
#types
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Notes(SQLAlchemyObjectType):
    class Meta:
        model = NotesModel

class FlagTable(SQLAlchemyObjectType):
    class Meta:
        model = FlagModel

class Token(SQLAlchemyObjectType):
    class Meta:
        model = TokenModel


#registration
class createUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()
    ok = graphene.Boolean()
    user = graphene.Field(User)

    def mutate(root, info, first_name, last_name, email, password):
        new_user = UserModel(first_name=first_name, last_name=last_name, email=email, is_admin=False, password=str(bcrypt.generate_password_hash(password), 'utf-8'))
        session.add(new_user)
        session.commit()
        ok = True
        return createUser(ok=ok, user=new_user)

class logIn(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()
    ok = graphene.Boolean()
    tokens = graphene.Field(Token)
    def mutate(root, info, email, password):
        user = session.query(UserModel).filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_tokens = create_access_token(identity=email)
            refresh_token = create_refresh_token(identity=email)
            new_token = TokenModel(access_token=access_tokens, refresh_token=refresh_token, user=email)
            session.add(new_token)
            session.commit()
            ok=True
            return logIn(ok=ok, tokens=new_token)
        else:
            raise Exception('email or password Incorrect')
class addNote(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        body = graphene.String()
    ok = graphene.Boolean()
    note = graphene.Field(Notes)

    @jwt_required()
    def mutate(root, info, title, body):
        uid = get_jwt_identity()
        #find user based on token
        user = session.query(UserModel).filter_by(email=uid).first()

        if uid == "admin@gmail.com":
            if user.notes:
                raise Exception('Cant add more notes')
            else:
                new_note = NotesModel(title=title, body=body, user=user)
                session.add(new_note)
                session.commit()
                ok = True
                return addNote(ok=ok, note=new_note)
        else:
            new_note = NotesModel(title=title, body=body, user=user)
            session.add(new_note)
            session.commit()
            ok = True
            return addNote(ok=ok, note=new_note)

class updateNote(graphene.Mutation):
    class Arguments:
        note_id = graphene.Int()
        title = graphene.String()
        body = graphene.String()
    ok = graphene.Boolean()
    note = graphene.Field(Notes)

    @jwt_required()
    def mutate(root, info, note_id, title: Optional[str]=None, body: Optional[str]=None):
        email=get_jwt_identity()
        note = session.query(NotesModel).filter_by(id=note_id).first()
        userl = session.query(UserModel).filter_by(email=email).first()

        try:
            noty = note.user_id
        except:
            raise Exception('The selected note_id doesnt exist')
        if note.user_id == userl.id:
            if note_id != 1:
                if not title:
                    note.body = body
                elif not body:
                    note.title = title
                else:
                    note.title = title
                    note.body = body
                session.commit()
                ok = True
                return updateNote(ok=ok, note=note)
            else:
                raise Exception('Cant update this note')
        else:
            raise Exception('Not enough permissions to update')

class deleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
    ok = graphene.Boolean()
    note = graphene.Field(Notes)

    @jwt_required()
    def mutate(root, info, id):
        email=get_jwt_identity()
        if compare_uids(id, email):
            if id != 1:
                session.delete(note)
                ok = True
                note = note
                session.commit()
                return deleteNote(ok=ok, note=note)
            else:
                raise Exception('Cant delete this note')
        else:
            raise Exception('Not enough permissions to delete')

class updateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        last_name = graphene.String()
        password = graphene.String()
    ok = graphene.Boolean()
    user = graphene.Field(User)

    @jwt_required()
    def mutate(root, info, id, last_name: Optional[str]=None, password: Optional[str]=None):
        user = session.query(UserModel).filter_by(id=id).first()
        try:
            user.last_name
        except:
            raise Exception('User id does not exist')
        if not last_name:
            user.password = str(bcrypt.generate_password_hash(password), 'utf-8')
        elif not password:
            user.last_name = last_name
        else:
            user.last_name = last_name
            user.password = str(bcrypt.generate_password_hash(password), 'utf-8')
        session.commit()
        ok = True
        return updateUser(ok=ok, user=user)

class Mutations(graphene.ObjectType):
    addNote = addNote.Field()
    updateNote = updateNote.Field()
    deleteNote = deleteNote.Field()
    create_User = createUser.Field()
    logIn = logIn.Field()
    updateUser = updateUser.Field()
    
class Query(graphene.ObjectType):
    #find single note
    findNote = graphene.Field(Notes, id=graphene.Int())

    #get all notes by user
    user_notes = graphene.List(Notes)

    @jwt_required()
    def resolve_user_notes(root, info):
        #find user with uid from token
        uid = get_jwt_identity()
        user = session.query(UserModel).filter_by(email=uid).first()
        return user.notes

    @jwt_required()
    def resolve_findNote(root, info, id):
        mail = get_jwt_identity()
        if compare_uids(id, mail):
            return session.query(NotesModel).filter_by(id=id).first()
        else:
            raise Exception('Not enough permissions search this note')

    getusers = graphene.List(User)
    get_flag = graphene.List(FlagTable)

    def resolve_getusers(root, info):
        return session.query(UserModel).filter_by(is_admin=False).all()

        

    def resolve_get_flag(root, info):
        return session.query(FlagModel).all()

schema = graphene.Schema(query=Query, mutation=Mutations)

def compare_uids(uid1, mail):
    note = session.query(NotesModel).filter_by(id=uid1).first()
    userl = session.query(UserModel).filter_by(email=mail).first()
    try:
        note.user_id
    except:
        raise Exception('note id not found')
    if note.user_id == userl.id:
        return True