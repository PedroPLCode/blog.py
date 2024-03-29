# Blog.py with simple SQL database

## Temporaru user:

```shell
login: admin
passwd: admin
```

## Endpoints:

```shell
Endpoint          Methods    Rule                       
----------------  ---------  ---------------------------
create_new_entry  GET, POST  /new-post/                 
delete_entry      POST       /delete-post/<int:entry_id>
edit_entry        GET, POST  /edit-post/<int:entry_id>  
homepage_view     GET        /                          
list_drafts       GET        /drafts/                   
login             GET, POST  /login/                    
logout            GET, POST  /logout/                   
search_drafts     GET        /search_drafts/            
search_posts      GET        /search/                   
static            GET        /templates/<path:filename> 
```

## Data Base setup:

init db:
```shell
flask db init
```

prep db migration:
```shell
flask db migrate
```

migrate db:
```shell
flask db upgrade
```