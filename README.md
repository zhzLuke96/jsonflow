# jsonflow

aim to Understand GraphQL

# todos

-   ~~reduce_flow...~~
-   ~~py eval~~
-   ~~auto foreign key~~
-   ~~plugin function~~
-   cache
-   auto association table
-   middleware,hook
-   other vector(遗忘的需求...)

# example

### query task

request:

```json
{
    "[user_arr]": {
        "!nick_name": "like 'admin_%'",
        "!sex": "= 'male'",
        "name": "user.nick_name",
        "id": "user.u_id",
        "amount": "user.u_amount",
        "geek_rank": "calc(int(amount) * int(id))",
        "?rich": "amount > 100",
        "...": "user",
        "{orders}": {
            "...": "orders"
        }
    }
}
```

response:

GET /query http/1.1

```json
{
    "user_arr": [{
            "?rich": "False",
            "age": 10,
            "amount": 100,
            "geek_rank": 200,
            "id": 2,
            "name": "admin_zhz",
            "orders": {
                "content": "222",
                "id": 2
            },
            "orders_id": 2,
            "sex": "male"
        },
        {
            "?rich": "True",
            "age": 18,
            "amount": 1000,
            "geek_rank": 4000,
            "id": 4,
            "name": "admin_yoo",
            "orders": "NOT FOUND",
            "orders_id": "None",
            "sex": "male"
        }
    ]
}
```

### watch task

request:

```json
{
    "{sys_status}":{
        "cpu":"%cpu_status",
        "memory_free":"%memory_status"
    }
}
```

response:

```json
{
    "sys_status": {
        "cpu": 13.4,
        "memory_free": 68.7
    }
}
```

### other

```json
{
    "[female_arr]":{
        "name":"user.name",
        "id":"user.id",
        "amount":"user.amount",
        "!sex":"is not 'male'",
        "!age":">18 and <35",
        "?addr":"in ['shanghai','shengzheng']"
    }
}
```

# 后
算那么点意思吧，但是问题也很多，直接写入sql直接执行py，易用性确实高，带来的注入问题也是很蛋疼的（也许是时候欣赏一波graphql的实现了）
