# tiny-lastfm-analyzer-backend
Backend for tiny-lastfm-analyzer made with Flask.

The data is fetched from the lastfm API with the help of pyLast package.  
Then it is groupped and analyzed with Pandas.  
At the end it's tailored to the needs of frontend. Artist's images are fetched with lastfmcache package.  

"Production" server made with gunicorn.  

It should be available at: https://tiny-lastfm-analyzer.up.railway.app/  
(Unless I run out of railway free tier credits lol)  

Disclaimer: I'm aware the timezone offset is far from being perfect. Might fix it later.  
