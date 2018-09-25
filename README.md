# jsonflow
aim to Understand GraphQL

# todos
- reduce_flow...
- py eval
- other vector
- auto foreign key
- plugin function

# example
```json
{
    "{sys_status}":{
        "cpu":"%cpu_status",
        "gpu":"%gpu_status",
        "memory":"calc(%memory_now / %memory_full)",
    }
}
```

```json
{
    "[user_arr]":{
        "name":"user.name",
        "id":"user.id",
        "amount":"user.amount",
        "[other]":"user...",
        "{record}":{
            "{last}":"top(record)",
            "[other]":"record..."
        }
    }
}
```

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

```json
{
    "{article}":{
        "!id":"2",
        "...":"article",
        "tag_count":"count(tags)",
        "[tags]":{
            "...":"tags"
        }
    }
}
{
    "{article...}":{
        "!id":"2",
        "tag_count":"count(tags)",
        "[tags...]":{}
    }
}
{
    "{article...}":{
        "tag_count":"count(tags)",
        "[tags...]":{},
        "!java":"in tags"
    }
}
```
