下面提供一个简单的 Chrome 浏览器插件示例，它会在每个页面加载时注入一个内容脚本，重写了 XMLHttpRequest 和 fetch 方法，将调用记录下来，并在页面右侧展示一个侧边栏，实时显示调用过的 xhr/fetch 接口，最新的记录排在最上方。

---

### manifest.json

这是插件的配置文件（基于 Manifest V3），它指定了在哪些页面注入内容脚本。

```json
{
  "manifest_version": 3,
  "name": "Network Monitor",
  "version": "1.0",
  "description": "实时展示页面中调用的 xhr 和 fetch 接口",
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ],
  "permissions": []
}
```

---

### content.js

这个脚本会在页面加载后自动执行。它重写了 XMLHttpRequest 和 fetch，并构建了一个固定在页面右侧的美观面板，显示每次调用的请求信息。你可以根据需要进一步美化界面和扩展功能。

```javascript
(function () {
  // 用于存储网络调用记录，最新记录放在数组最前面
  const networkCalls = [];

  // 更新侧边栏面板显示
  function updatePanel() {
    const container = document.getElementById("network-panel");
    if (!container) return;

    // 清空原有内容（保留标题部分）
    container.querySelector(".panel-content").innerHTML = "";

    // 遍历所有记录，最新的在上面
    networkCalls.forEach(call => {
      const item = document.createElement("div");
      item.className = "network-item";
      item.innerHTML = `
        <div><strong>[${call.type}]</strong> ${call.method}</div>
        <div class="url">${call.url}</div>
        <div class="time">${new Date(call.time).toLocaleTimeString()}</div>
      `;
      container.querySelector(".panel-content").appendChild(item);
    });
  }

  // 添加一条网络调用记录，并更新面板
  function addNetworkCall(details) {
    // 新的记录插入数组头部
    networkCalls.unshift(details);
    updatePanel();
  }

  // 拦截 XMLHttpRequest 调用
  const OriginalXHR = window.XMLHttpRequest;
  function XHRProxy() {
    const xhr = new OriginalXHR();
    let url = "";
    let method = "";

    // 重写 open 方法，记录请求方法和 url
    const originalOpen = xhr.open;
    xhr.open = function (m, u, ...args) {
      method = m;
      url = u;
      return originalOpen.apply(xhr, [m, u, ...args]);
    };

    // 重写 send 方法，在发送请求时记录调用信息
    const originalSend = xhr.send;
    xhr.send = function (...args) {
      addNetworkCall({
        type: "XHR",
        method,
        url,
        time: Date.now()
      });
      return originalSend.apply(xhr, args);
    };

    return xhr;
  }
  window.XMLHttpRequest = XHRProxy;

  // 拦截 fetch 调用
  const originalFetch = window.fetch;
  window.fetch = function (...args) {
    let url = "";
    let method = "GET";

    // args[0] 可以是 Request 对象或者 url 字符串
    if (typeof args[0] === "string") {
      url = args[0];
    } else if (args[0] && args[0].url) {
      url = args[0].url;
    }
    // 如果传入 options，可能包含 method
    if (args[1] && args[1].method) {
      method = args[1].method;
    }

    addNetworkCall({
      type: "Fetch",
      method,
      url,
      time: Date.now()
    });

    return originalFetch.apply(this, args);
  };

  // 创建一个固定的侧边栏面板
  function createPanel() {
    const panel = document.createElement("div");
    panel.id = "network-panel";
    panel.innerHTML = `
      <div class="panel-header">
        <h2>网络调用监控</h2>
      </div>
      <div class="panel-content"></div>
    `;
    document.body.appendChild(panel);

    // 内联 CSS 样式，美化侧边栏
    const style = document.createElement("style");
    style.textContent = `
      #network-panel {
        position: fixed;
        top: 0;
        right: 0;
        width: 320px;
        height: 100%;
        background: rgba(0, 0, 0, 0.85);
        color: #fff;
        font-family: "Segoe UI", sans-serif;
        font-size: 12px;
        z-index: 9999;
        overflow-y: auto;
        box-shadow: -2px 0 8px rgba(0, 0, 0, 0.5);
      }
      #network-panel .panel-header {
        padding: 10px;
        background: #444;
        border-bottom: 1px solid #666;
        text-align: center;
      }
      #network-panel .panel-header h2 {
        margin: 0;
        font-size: 16px;
      }
      #network-panel .panel-content {
        padding: 10px;
      }
      #network-panel .network-item {
        margin-bottom: 10px;
        padding-bottom: 10px;
        border-bottom: 1px solid #666;
      }
      #network-panel .network-item .url {
        word-break: break-all;
        color: #a8d0e6;
      }
      #network-panel .network-item .time {
        font-size: 10px;
        color: #ccc;
      }
    `;
    document.head.appendChild(style);
  }

  // 初始化面板
  createPanel();
})();
```

---

### 说明

1. **监控逻辑**  
   - 对于 **XMLHttpRequest**：重写了 `open` 和 `send` 方法，获取请求的方法和 URL，并在 `send` 时调用 `addNetworkCall` 记录信息。  
   - 对于 **fetch**：重写了 `window.fetch` 方法，在调用前解析参数中的 URL 和请求方法，然后记录调用信息。

2. **数据存储与排序**  
   - 每次记录调用信息时，将最新的记录插入数组头部，从而保证显示时最新的在最上方。

3. **界面展示**  
   - 通过在页面中创建一个固定的侧边栏 `<div id="network-panel">` 来展示调用信息。  
   - 使用内联 CSS 实现美观的展示效果（你可以根据需要进一步修改样式）。

4. **注入时机**  
   - 该插件为内容脚本形式，匹配所有页面（`"<all_urls>"`），每次页面刷新或者进入新页面时都会自动注入并生效。

---

将以上两个文件打包为 Chrome 插件，然后在 Chrome 的扩展程序管理界面中加载该插件（启用开发者模式后加载已解压的扩展程序）。这样，当你刷新页面或进入新页面时，就可以在右侧看到实时的 xhr/fetch 调用记录。

希望这能满足你的需求！
