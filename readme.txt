server {
    listen       80;
    server_name  mdota.dev2.haalee.com;
    merge_slashes off;
                    
    location ^~ /media/ {
        root /opt/sites/mdota.dev2.haalee.com;
    }
                                         
    location  /favicon.ico {
        empty_gif;
        access_log off;
    }
                            
    location  /tmp/ {
        root /opt/sites/mdota.dev2.haalee.com;
    }
                    
    location  /robots.txt {
        empty_gif;
        access_log off;
    }
                            
    location / {
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_set_header Host $http_host;
         proxy_set_header Environ_name 'develop:0.0.2';
         proxy_redirect off;
         proxy_buffering off;
                                                     
         proxy_pass   http://127.0.0.1:58500;
    }
    access_log  logs/access_mdota.dev2.haalee.com;
    error_log   logs/error_mdota.dev2.haalee.com;
}
