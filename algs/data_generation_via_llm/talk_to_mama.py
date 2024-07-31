def talk_to_mama_on_the_local():
    """
    """
    pass

def talk_to_mama_on_the_cloud():
    """
    """
    import requests
    import os

    url = os.environ["LINKAI_HOST"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["LINKAI_KEY"]
    }
    body = {
        "app_code": os.environ["LINKAI_CODE_1"],
        "messages": [
            {
                "role": "user",
                "content": "Give me 99 user profiles, each user profile should contain username, email, phone, interest tags, gender, age, occupation, annual_income. All in json format. The FULL output."
            }
        ]
    }
    res = requests.post(url, json=body, headers=headers)
    if res.status_code == 200:
        reply_text = res.json().get("choices")[0]['message']['content']
        print(reply_text)
    else:
        error = res.json().get("error")
        print(f"请求异常, 错误码={res.status_code}, 错误类型={error.get('type')}, 错误信息={error.get('message')}")

def talk_to_db():
    from typing import Optional

    from sqlmodel import Field, Session, SQLModel, create_engine, select


    class Hero(SQLModel, table=True):
        id: Optional[int] = Field(default=None, primary_key=True)
        name: str
        secret_name: str
        age: Optional[int] = None

    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

    engine = create_engine("sqlite:///database.db")

    '''
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()
    '''

    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        hero = session.exec(statement).first()
        print(hero)