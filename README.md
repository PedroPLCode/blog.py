# Blog.py with simple SQL database

## [Live Link to Project on Replit](https://6ecd70b3-4f2e-4d0e-98f4-73d36f0c8004-00-3iztk1pxk76j0.spock.replit.dev/)

## Temporary user:

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