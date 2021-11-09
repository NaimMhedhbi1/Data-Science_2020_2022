/*

Sign up here http://bit.ly/freescraperAPIkey and get the API Key

Refer Docs for detailed documentation http://bit.ly/scraperDocs

*/

function scrapeInstaFollowers() {

    var url1 = "http://api.scraperapi.com?api_key=b0ea57f1dad1e546b281476c6e1c8935&url=http://httpbin.org/ip"
    var url2 = "https://www.instagram.com/_aamirkhan"
    
    var finalUrl = url1+url2;
    
    var getContent = UrlFetchApp.fetch(finalUrl).getContentText();
    var getContent = getContent.trim();
    var followerRegex = /meta property="og:description".*Followers/gi
    
    var getFollowers = getContent.match(followerRegex)
    var followers = getFollowers[0].replace('meta property="og:description" content="',"")
    Logger.log(followers)
    
    }