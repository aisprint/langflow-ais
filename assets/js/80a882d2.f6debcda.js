"use strict";(self.webpackChunkdocusaurus=self.webpackChunkdocusaurus||[]).push([[610],{3905:(e,t,n)=>{n.d(t,{Zo:()=>p,kt:()=>y});var r=n(7294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function a(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function i(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?a(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):a(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function l(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},a=Object.keys(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);for(r=0;r<a.length;r++)n=a[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var s=r.createContext({}),m=function(e){var t=r.useContext(s),n=t;return e&&(n="function"==typeof e?e(t):i(i({},t),e)),n},p=function(e){var t=m(e.components);return r.createElement(s.Provider,{value:t},e.children)},c="mdxType",u={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},d=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,a=e.originalType,s=e.parentName,p=l(e,["components","mdxType","originalType","parentName"]),c=m(n),d=o,y=c["".concat(s,".").concat(d)]||c[d]||u[d]||a;return n?r.createElement(y,i(i({ref:t},p),{},{components:n})):r.createElement(y,i({ref:t},p))}));function y(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var a=n.length,i=new Array(a);i[0]=d;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[c]="string"==typeof e?e:o,i[1]=l;for(var m=2;m<a;m++)i[m]=n[m];return r.createElement.apply(null,i)}return r.createElement.apply(null,n)}d.displayName="MDXCreateElement"},3414:(e,t,n)=>{n.d(t,{Z:()=>i});var r=n(7294),o=n(941),a=n(4996);const i=e=>{let{alt:t,sources:n}=e;const[i,l]=(0,r.useState)(!1),s=e=>{"Escape"===e.key&&l(!1)};return(0,r.useEffect)((()=>(i?document.addEventListener("keydown",s):document.removeEventListener("keydown",s),()=>{document.removeEventListener("keydown",s)})),[i]),r.createElement("div",{className:"zoomable-image "+(i?"fullscreen":""),onClick:()=>{l(!i)}},r.createElement(o.Z,{className:"zoomable-image-inner",alt:t,sources:{light:(0,a.Z)(n.light),dark:(0,a.Z)(n.dark)}}))}},8361:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>m,contentTitle:()=>l,default:()=>d,frontMatter:()=>i,metadata:()=>s,toc:()=>p});var r=n(7462),o=(n(7294),n(3905)),a=(n(941),n(4996),n(3414));const i={},l="MidJourney Prompt Chain",s={unversionedId:"midjourney-prompt-chain",id:"midjourney-prompt-chain",title:"MidJourney Prompt Chain",description:"The MidJourneyPromptChain can be used to generate imaginative and detailed MidJourney prompts.",source:"@site/docs/midjourney-prompt-chain.mdx",sourceDirName:".",slug:"/midjourney-prompt-chain",permalink:"/langflow/midjourney-prompt-chain",draft:!1,tags:[],version:"current",frontMatter:{},sidebar:"docs",previous:{title:"Buffer Memory",permalink:"/langflow/buffer-memory"},next:{title:"CSV Loader",permalink:"/langflow/csv-loader"}},m={},p=[{value:"\u26d3\ufe0f LangFlow Example",id:"\ufe0f-langflow-example",level:2},{value:'<a target="_blank" href="json_files/MidJourney_Prompt_Chain.json" download>Download Flow</a>',id:"download-flow",level:4}],c={toc:p},u="wrapper";function d(e){let{components:t,...n}=e;return(0,o.kt)(u,(0,r.Z)({},c,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"midjourney-prompt-chain"},"MidJourney Prompt Chain"),(0,o.kt)("p",null,"The ",(0,o.kt)("inlineCode",{parentName:"p"},"MidJourneyPromptChain")," can be used to generate imaginative and detailed MidJourney prompts."),(0,o.kt)("p",null,"For example, type something like:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-bash"},"Dragon\n")),(0,o.kt)("p",null,"And get a response such as:"),(0,o.kt)("pre",null,(0,o.kt)("code",{parentName:"pre",className:"language-text"},"Imagine a mysterious forest, the trees are tall and ancient, their branches reaching up to the sky. Through the darkness, a dragon emerges from the shadows, its scales shimmering in the moonlight. Its wingspan is immense, and its eyes glow with a fierce intensity. It is a majestic and powerful creature, one that commands both respect and fear.\n")),(0,o.kt)("admonition",{type:"tip"},(0,o.kt)("p",{parentName:"admonition"},"Notice that the ",(0,o.kt)("inlineCode",{parentName:"p"},"ConversationSummaryMemory")," stores a summary of the conversation over time. Try using it to create better prompts as the conversation goes on.")),(0,o.kt)("h2",{id:"\ufe0f-langflow-example"},"\u26d3\ufe0f LangFlow Example"),(0,o.kt)(a.Z,{alt:"Docusaurus themed image",sources:{light:"img/midjourney-prompt-chain.png"},mdxType:"ZoomableImage"}),(0,o.kt)("h4",{id:"download-flow"},(0,o.kt)("a",{target:"\\_blank",href:"json_files/MidJourney_Prompt_Chain.json",download:!0},"Download Flow")),(0,o.kt)("admonition",{title:"LangChain Components \ud83e\udd9c\ud83d\udd17",type:"note"},(0,o.kt)("ul",{parentName:"admonition"},(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("a",{parentName:"li",href:"https://python.langchain.com/docs/modules/model_io/models/llms/integrations/openai"},(0,o.kt)("inlineCode",{parentName:"a"},"OpenAI"))),(0,o.kt)("li",{parentName:"ul"},(0,o.kt)("a",{parentName:"li",href:"https://python.langchain.com/docs/modules/memory/how_to/summary"},(0,o.kt)("inlineCode",{parentName:"a"},"ConversationSummaryMemory"))))))}d.isMDXComponent=!0}}]);