<!-- MySQL Shell Commands -->

> \sql
> \connect root@localhost

<!-- Enter password if not saved -->

> show databases;

    +--------------------+
    | Database           |
    +--------------------+
    | flask_tut          |
    | information_schema |
    | mysql              |
    | our_users          |
    | performance_schema |
    | sakila             |
    | sys                |
    | world              |
    +--------------------+

> use flask_tut;
> show tables;
> select \* from member; <!-- No "\" in command  -->

    +----+----------+----------+---------------+---------------------+
    | id | username | password | email         | join_date           |
    +----+----------+----------+---------------+---------------------+
    |  1 | aman     | password | aman@test.com | 2022-03-07 00:00:00 |
    |  2 | Jane     | testuser | jane@test.com | 2022-03-07 00:00:00 |
    +----+----------+----------+---------------+---------------------+

<!-- Python Shell Commands -->
<!-- prettier-ignore-start -->
>>> from app import db
>>> from app import Member
>>> from datetime import date
>>> aman=Member(username='aman',password='password',email='aman@test.com',join_date=date.today())
<!-- add db -->
>>> db.session.add(aman)
>>> db.session.commit()
<!-- update db -->
>>> aman.password='secretpass'
>>> db.session.commit()
<!-- delete db -->
>>> db.session.delete(aman)
>>> db.session.commit()

<!-- query ORM -->
>>> results=Member.query.all()
>>> results
>>> for r in results:
        print(r.username) <!-- r.email and so on -->
>>> aman = Member.query.filter_by(username='aman').first() <!-- "aman" is SQLAlchemy object -->
>>> print(aman.email)
>>> jane=Member.query.filter(Member.username == 'Jane').first()
>>> print(jane.username)
Jane
>>> print(jane.email)
foreverjane@yahoo.com
>>> q1=Member.query
>>> q2=q1.filter(Member.username=='aman')
>>> q1.all()
[<Member 'Jane'>, <Member 'aman'>, <Member 'john'>]
>>> q2.all()
[<Member 'aman'>]
>>> q3=q2.filter(Member.username=='notexists')
>>> q3.all()
[]

<!-- not equals -->
>>> q=Member.query.filter(Member.username!='aman').all()
>>> q
[<Member 'Jane'>, <Member 'john'>]
>>> q1=Member.query.filter(Member.email!='john@test.com').all()
>>> q1

<!-- like -->
>>> like_query=Member.query.filter(Member.username.like('%am%'))
>>> like_query
<flask_sqlalchemy.BaseQuery object at 0x0000018B9E0965F0>
>>> like_query.all()
[<Member 'aman'>]

<!-- Null -->
>>> karan=Member(username='karan',password='testuser')
>>> db.session.add(karan)
>>> db.session.commit()
>>> q=Member.query.filter(Member.email==None).all()
>>> q
[<Member 'karan'>]
>>> q=Member.query.filter(Member.email!=None).all()
>>> q
[<Member 'Jane'>, <Member 'aman'>, <Member 'john'>]
<!-- prettier-ignore-end -->
