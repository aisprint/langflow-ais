"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[763],{3905:(e,t,n)=>{n.d(t,{Zo:()=>m,kt:()=>d});var r=n(7294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),c=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},m=function(e){var t=c(e.components);return r.createElement(s.Provider,{value:t},e.children)},p="mdxType",u={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},f=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,a=e.originalType,s=e.parentName,m=l(e,["components","mdxType","originalType","parentName"]),p=c(n),f=o,d=p["".concat(s,".").concat(f)]||p[f]||u[f]||a;return n?r.createElement(d,i(i({ref:t},m),{},{components:n})):r.createElement(d,i({ref:t},m))}));function d(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=n.length,i=new Array(a);i[0]=f;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[p]="string"==typeof e?e:o,i[1]=l;for(var c=2;c<a;c++)i[c]=n[c];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}f.displayName="MDXCreateElement"},3414:(e,t,n)=>{n.d(t,{Z:()=>i});var r=n(7294),o=n(941),a=n(4996);const i=e=>{let{alt:t,sources:n}=e;const[i,l]=(0,r.useState)(!1),s=e=>{"Escape"===e.key&&l(!1)};return(0,r.useEffect)((()=>(i?document.addEventListener("keydown",s):document.removeEventListener("keydown",s),()=>{document.removeEventListener("keydown",s)})),[i]),r.createElement("div",{className:"zoomable-image "+(i?"fullscreen":""),onClick:()=>{l(!i)}},r.createElement(o.Z,{className:"zoomable-image-inner",alt:t,sources:{light:(0,a.Z)(n.light),dark:(0,a.Z)(n.dark)}}))}},276:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>l,default:()=>f,frontMatter:()=>i,metadata:()=>s,toc:()=>m});var r=n(7462),o=(n(7294),n(3905)),a=(n(941),n(4996),n(3414));const i={},l="Buffer Memory",s={unversionedId:"buffer-memory",id:"buffer-memory",title:"Buffer Memory",description:"For certain applications, retaining past interactions is crucial. For that, chains and agents may accept a memory component as one of their input parameters. The ConversationBufferMemory component is one of them. It stores messages and extracts them into variables.",source:"@site/docs/buffer-memory.mdx",sourceDirName:".",slug:"/buffer-memory",permalink:"/langflow/buffer-memory",draft:!1,tags:[],version:"current",frontMatter:{},sidebar:"docs",previous:{title:"Conversation Chain",permalink:"/langflow/conversation-chain"},next:{title:"MidJourney Prompt Chain",permalink:"/langflow/midjourney-prompt-chain"}},c={},m=[{value:"\u26d3\ufe0f LangFlow Example",id:"\ufe0f-langflow-example",level:2},{value:'<a target="_blank" href="json_files/Buffer_Memory.json" download>Download Flow</a>',id:"download-flow",level:4}],p={toc:m},u="wrapper";function f(e){let{components:t,...n}=e;return(0,o.kt)(u,(0,r.Z)({},p,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"buffer-memory"},"Buffer Memory"),(0,o.kt)("p",null,"For certain applications, retaining past interactions is crucial. For that, chains and agents may accept a memory component as one of their input parameters. The ",(0,o.kt)("inlineCode",{parentName:"p"},"ConversationBufferMemory")," component is one of them. It stores messages and extracts them into variables."),(0,o.kt)("h2",{id:"\ufe0f-langflow-example"},"\u26d3\ufe0f LangFlow Example"),(0,o.kt)(a.Z,{alt:"Docusaurus themed image",sources:{light:"img/buffer-memory.png"},mdxType:"ZoomableImage"}),(0,o.kt)("h4",{id:"download-flow"},(0,o.kt)("a",{target:"\\_blank",href:"json_files/Buffer_Memory.json",download:!0},"Download Flow")),(0,o.kt)("admonition",{title:"LangChain Components \ud83e\udd9c\ud83d\udd17",type:"note"},(0,o.kt)("ul",{parentName:"admonition"},(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("a",{parentName:"li",href:"https://python.langchain.com/docs/modules/memory/how_to/buffer"},(0,o.kt)("inlineCode",{parentName:"a"},"ConversationBufferMemory"))),(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("a",{parentName:"li",href:"https://python.langchain.com/docs/modules/chains/"},(0,o.kt)("inlineCode",{parentName:"a"},"ConversationChain"))),(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("a",{parentName:"li",href:"https://python.langchain.com/docs/modules/model_io/models/chat/integrations/openai"},(0,o.kt)("inlineCode",{parentName:"a"},"ChatOpenAI"))))))}f.isMDXComponent=!0}}]);