chrome.browserAction.onClicked.addListener((tab) => {
  chrome.tabs.executeScript(tab.id, {
    code: `
      {
        const script = document.createElement('script');
        script.textContent = \`
          {
            const host = location.host;
            const site = host.split('.')[1];
            let content = '';
            if (site === 'pixnet') {
              content = jQuery('.article-content-inner').text().trim();
            } else if (site === 'ptt') {
              content = $('#main-content').clone().children('div').remove().end().text();
            } else if (site === 'xuite') {
              content = $('#content_all').text();
            }
            console.log(content);

            fetch('https://p1wl51hz14.execute-api.us-west-2.amazonaws.com/prod/yehpeiwenDetect', {
              method: 'post',
              headers: {
                'Content-type': 'application/json'
              },
              body: JSON.stringify({ context: content })
            })
              .then((res) => res.json())
              .then((data) => {
                if (data.success && !data.isSpam) {
                  document.body.innerHTML += \\\`
                    <div id="ypw-detect-result" style="
                      position: fixed;
                      bottom: 4%;
                      left: 50%;
                      margin-left: -120px;
                      width: 240px;
                      text-align: center;
                      height: 54px;
                      background-color: #43C6AC;
                      background: -webkit-linear-gradient(right, #43C6AC, #F8FFAE);
                      background: -o-linear-gradient(right, #43C6AC, #F8FFAE);
                      background: -moz-linear-gradient(right, #43C6AC, #F8FFAE);
                      background: linear-gradient(to right, #43C6AC, #F8FFAE);
                      box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
                      color: white;
                      line-height: 54px;
                      font-size: 16px;
                      z-index: 999;
                    ">
                    <svg style="vertical-align: text-bottom;" fill="#ffffff" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M0 0h24v24H0z" fill="none"/>
                      <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
                    </svg>
                      您可以安心瀏覽！
                    </div>
                  \\\`;
                } else {
                  document.body.innerHTML += \\\`
                  <div id="ypw-detect-result" style="
                    position: fixed;
                    bottom: 4%;
                    left: 50%;
                    margin-left: -120px;
                    width: 280px;
                    text-align: center;
                    height: 54px;
                    background-color: #16BFFD;
                    background: -webkit-linear-gradient(right, #16BFFD, #CB3066);
                    background: -o-linear-gradient(right, #16BFFD, #CB3066);
                    background: -moz-linear-gradient(right, #16BFFD, #CB3066);
                    background: linear-gradient(to right, #16BFFD, #CB3066);
                    box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
                    color: white;
                    line-height: 54px;
                    font-size: 16px;
                    z-index: 999;
                  ">
                  <svg style="vertical-align: text-bottom;" fill="#ffffff" height="20" viewBox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0 0h24v24H0z" fill="none"/>
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM4 12c0-4.42 3.58-8 8-8 1.85 0 3.55.63 4.9 1.69L5.69 16.9C4.63 15.55 4 13.85 4 12zm8 8c-1.85 0-3.55-.63-4.9-1.69L18.31 7.1C19.37 8.45 20 10.15 20 12c0 4.42-3.58 8-8 8z"/>
                  </svg>
                    您可能是業配文的受害者。
                  </div>
                  \\\`;
                }
              });
          }
        \`;
        document.body.appendChild(script);
      }
    `,
  });
});
