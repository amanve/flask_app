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

<!-- prettier-ignore-start  -->
> select * from member;


    +----+----------+----------+---------------+---------------------+
    | id | username | password | email         | join_date           |
    +----+----------+----------+---------------+---------------------+
    |  1 | aman     | password | aman@test.com | 2022-03-07 00:00:00 |
    |  2 | Jane     | testuser | jane@test.com | 2022-03-07 00:00:00 |
    +----+----------+----------+---------------+---------------------+

> select * from `order`; <!-- "order" is builtin function so it is enclosed in `backticks` -->
> select * from course;

    +----+------------+
    | id | name       |
    +----+------------+
    |  1 | Python     |
    |  2 | C++        |
    |  3 | JavaScript |
    +----+------------+

> select * from member;
    +----+----------+----------+-----------------------+---------------------+
    | id | username | password | email                 | join_date           |
    +----+----------+----------+-----------------------+---------------------+
    |  2 | Jane     | testuser | foreverjane@yahoo.com | 2022-03-07 00:00:00 |
    |  3 | aman     | testpass | aman@test.com         | 2022-03-07 00:00:00 |
    |  4 | john     | password | john@test.com         | 2022-03-07 00:00:00 |
    |  5 | karan    | testuser | NULL                  | NULL                |
    +----+----------+----------+-----------------------+---------------------+

> select * from course;
    +----+------------+
    | id | name       |
    +----+------------+
    |  1 | Python     |
    |  2 | C++        |
    |  3 | JavaScript |
    +----+------------+

> select member.id, member.username from `member`;
    +----+----------+
    | id | username |
    +----+----------+
    |  3 | aman     |
    |  2 | Jane     |
    |  4 | john     |
    |  5 | karan    |
    +----+----------+

> select mem.id, mem.username, course.name as course_name from `member` as mem left join `user_courses` as uc on mem.id = uc.member_id left join `course` as course on uc.member_id = course.id;
<!-- prettier-ignore-end  -->

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
<!-- And Query -->
>>> q=Member.query.filter(Member.username=='aman').filter(Member.email=='jane@test.com').all()
>>> q
[]
>>> q=Member.query.filter(Member.username=='aman').filter(Member.email=='aman@test.com').all()
>>> q
[<Member 'aman'>]
>>> q=Member.query.filter(db.and_(Member.username=='aman',Member.email=='aman@test.com')).all()
>>> q
[<Member 'aman'>]

<!-- Or query -->
>>> q=Member.query.filter(db.or_(Member.username=='aman',Member.email=='jane@test.com')).all()
>>> q
[<Member 'aman'>]
>>> q=Member.query.filter(db.or_(Member.username=='aman',Member.email=='john@test.com')).all()
>>> q
[<Member 'aman'>, <Member 'john'>]

<!-- Order_by Query -->
>>> Member.query.order_by(Member.username).all()
[<Member 'aman'>, <Member 'Jane'>, <Member 'john'>, <Member 'karan'>]
>>> Member.query.order_by(Member.id).all()
[<Member 'Jane'>, <Member 'aman'>, <Member 'john'>, <Member 'karan'>]
>>> Member.query.order_by(Member.id).first()
<Member 'Jane'>
>>> q1=Member.query.filter(db.or_(Member.username=='aman',Member.username=='ne'))
>>> q1.all()
[<Member 'aman'>]
>>> q1.order_by(Member.username).all()
[<Member 'aman'>]

<!-- Limit Query -->
>>> Member.query.limit(2).all()
[<Member 'Jane'>, <Member 'aman'>]
>>> Member.query.order_by(Member.username).limit(2).all()
[<Member 'aman'>, <Member 'Jane'>]

<!-- Offset Query -->
>>> Member.query.offset(1).all()
[<Member 'aman'>, <Member 'john'>, <Member 'karan'>]
>>> Member.query.offset(2).all()
[<Member 'john'>, <Member 'karan'>]

<!-- Count Query -->
>>> Member.query.filter(db.or_(Member.username=='aman',Member.username=='jane')).count()
2
>>> Member.query.count()
4

<!-- Inequality Query -->
>>> q=Member.query.filter(Member.id>2).all()
>>> q
[<Member 'aman'>, <Member 'john'>, <Member 'karan'>]
>>> q1=Member.query.filter(Member.id<3).all()
>>> q1
[<Member 'Jane'>]
>>> q2=Member.query.filter(Member.email<'g').all()
>>> q2
[<Member 'Jane'>, <Member 'aman'>]

<!-- One to Many relationships -->
>>> Member.query.all()
[<Member 'Jane'>, <Member 'aman'>, <Member 'john'>, <Member 'karan'>]
>>> karan=Member.query.filter(Member.username=='karan').first()
>>> karan
<Member 'karan'>
>>> karan.id
5
>>> order1=Order(price=30,member_id=karan.id)
>>> db.session.add(order1)
>>> db.session.commit()
>>> karan.orders.all()

<!-- Many to many query -->
>>> from app import db,Member,Order,Course
>>> course1=Course(name='Python')
>>> course2=Course(name='C++')
>>> course3=Course(name='JavaScript')

>>> db.session.add(course1) 
>>> db.session.add(course2)
>>> db.session.add(course3)
>>> db.session.commit()

>>> course1.member
[]
>>> course2.member
[]
>>> course3.member
[]
>>> aman=Member.query.filter(Member.username=='aman').first()
>>> karan=Member.query.filter(Member.username=='karan').first()
>>> aman
<Member 'aman'>
>>> karan
<Member 'karan'>
>>> course1.member.append(aman)
>>> course1.member
[<Member 'aman'>]
>>> course1.member.append(karan)
>>> course1.member
[<Member 'aman'>, <Member 'karan'>]
>>> course2.member.append(aman)
>>> course3.member.append(karan)
>>> aman.courses.all()
[<Course 1>, <Course 2>]
>>> karan.courses.all()
[<Course 1>, <Course 3>]
>>> aman.courses.all()    
[<Course 1>, <Course 2>]
>>> course1.member
[<Member 'aman'>, <Member 'karan'>]
>>> db.session.commit()

<!-- prettier-ignore-end -->
