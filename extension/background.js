chrome.contextMenus.create(
    {
        "id": "my-ai-app",
        "title": "What is this?",
        "contexts": ["image"]
    }
)

chrome.contextMenus.onClicked.addListener(
    async (info) => {
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        const raw = JSON.stringify({ url: info["srcUrl"] });

        const requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        const response = await fetch("http://localhost:5000", requestOptions)

        const text = await response.text()

        chrome.notifications.create('NOTFICATION_ID', {
            type: 'basic',
            iconUrl: 'icon.png',
            title: 'Your prediction is ready',
            message: text,
            priority: 2
        })
    }
)