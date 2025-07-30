/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */const A=Symbol("Comlink.proxy"),I=Symbol("Comlink.endpoint"),M=Symbol("Comlink.releaseProxy"),E=Symbol("Comlink.finalizer"),m=Symbol("Comlink.thrown"),W=e=>typeof e=="object"&&e!==null||typeof e=="function",T={canHandle:e=>W(e)&&e[A],serialize(e){const{port1:r,port2:t}=new MessageChannel;return _(e,r),[t,[t]]},deserialize(e){return e.start(),F(e)}},v={canHandle:e=>W(e)&&m in e,serialize({value:e}){let r;return e instanceof Error?r={isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:r={isError:!1,value:e},[r,[]]},deserialize(e){throw e.isError?Object.assign(new Error(e.value.message),e.value):e.value}},x=new Map([["proxy",T],["throw",v]]);function C(e,r){for(const t of e)if(r===t||t==="*"||t instanceof RegExp&&t.test(r))return!0;return!1}function _(e,r=globalThis,t=["*"]){r.addEventListener("message",function o(n){if(!n||!n.data)return;if(!C(t,n.origin)){console.warn(`Invalid origin '${n.origin}' for comlink proxy`);return}const{id:i,type:p,path:l}=Object.assign({path:[]},n.data),d=(n.data.argumentList||[]).map(f);let s;try{const a=l.slice(0,-1).reduce((c,h)=>c[h],e),u=l.reduce((c,h)=>c[h],e);switch(p){case"GET":s=u;break;case"SET":a[l.slice(-1)[0]]=f(n.data.value),s=!0;break;case"APPLY":s=u.apply(a,d);break;case"CONSTRUCT":{const c=new u(...d);s=H(c)}break;case"ENDPOINT":{const{port1:c,port2:h}=new MessageChannel;_(e,h),s=U(c,[c])}break;case"RELEASE":s=void 0;break;default:return}}catch(a){s={value:a,[m]:0}}Promise.resolve(s).catch(a=>({value:a,[m]:0})).then(a=>{const[u,c]=b(a);r.postMessage(Object.assign(Object.assign({},u),{id:i}),c),p==="RELEASE"&&(r.removeEventListener("message",o),O(r),E in e&&typeof e[E]=="function"&&e[E]())}).catch(a=>{const[u,c]=b({value:new TypeError("Unserializable return value"),[m]:0});r.postMessage(Object.assign(Object.assign({},u),{id:i}),c)})}),r.start&&r.start()}function N(e){return e.constructor.name==="MessagePort"}function O(e){N(e)&&e.close()}function F(e,r){const t=new Map;return e.addEventListener("message",function(n){const{data:i}=n;if(!i||!i.id)return;const p=t.get(i.id);if(p)try{p(i)}finally{t.delete(i.id)}}),S(e,t,[],r)}function w(e){if(e)throw new Error("Proxy has been released and is not useable")}function j(e){return y(e,new Map,{type:"RELEASE"}).then(()=>{O(e)})}const g=new WeakMap,P="FinalizationRegistry"in globalThis&&new FinalizationRegistry(e=>{const r=(g.get(e)||0)-1;g.set(e,r),r===0&&j(e)});function D(e,r){const t=(g.get(r)||0)+1;g.set(r,t),P&&P.register(e,r,e)}function L(e){P&&P.unregister(e)}function S(e,r,t=[],o=function(){}){let n=!1;const i=new Proxy(o,{get(p,l){if(w(n),l===M)return()=>{L(i),j(e),r.clear(),n=!0};if(l==="then"){if(t.length===0)return{then:()=>i};const d=y(e,r,{type:"GET",path:t.map(s=>s.toString())}).then(f);return d.then.bind(d)}return S(e,r,[...t,l])},set(p,l,d){w(n);const[s,a]=b(d);return y(e,r,{type:"SET",path:[...t,l].map(u=>u.toString()),value:s},a).then(f)},apply(p,l,d){w(n);const s=t[t.length-1];if(s===I)return y(e,r,{type:"ENDPOINT"}).then(f);if(s==="bind")return S(e,r,t.slice(0,-1));const[a,u]=z(d);return y(e,r,{type:"APPLY",path:t.map(c=>c.toString()),argumentList:a},u).then(f)},construct(p,l){w(n);const[d,s]=z(l);return y(e,r,{type:"CONSTRUCT",path:t.map(a=>a.toString()),argumentList:d},s).then(f)}});return D(i,e),i}function V(e){return Array.prototype.concat.apply([],e)}function z(e){const r=e.map(b);return[r.map(t=>t[0]),V(r.map(t=>t[1]))]}const R=new WeakMap;function U(e,r){return R.set(e,r),e}function H(e){return Object.assign(e,{[A]:!0})}function b(e){for(const[r,t]of x)if(t.canHandle(e)){const[o,n]=t.serialize(e);return[{type:"HANDLER",name:r,value:o},n]}return[{type:"RAW",value:e},R.get(e)||[]]}function f(e){switch(e.type){case"HANDLER":return x.get(e.name).deserialize(e.value);case"RAW":return e.value}}function y(e,r,t,o){return new Promise(n=>{const i=J();r.set(i,n),e.start&&e.start(),e.postMessage(Object.assign({id:i},t),o)})}function J(){return new Array(4).fill(0).map(()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16)).join("-")}self.window=self;let k=null;async function B(){return k||(k=import("https://cdn.jsdelivr.net/pyodide/v0.27.2/full/pyodide.mjs").then(e=>e.loadPyodide)),k}class G{constructor(){console.log("[Worker] Initializing PreswaldWorker"),this.pyodide=null,this.isInitialized=!1,this.activeScriptPath=null,this.components={}}async initializePyodide(){console.log("[Worker] Starting Pyodide initialization");try{const r=await B();return console.log("[Worker] About to call loadPyodide"),this.pyodide=await r({indexURL:"https://cdn.jsdelivr.net/pyodide/v0.27.2/full/"}),console.log("[Worker] loadPyodide resolved"),console.log("[Worker] Setting browser mode flag"),this.pyodide.runPython(`
                import js
                js.window.__PRESWALD_BROWSER_MODE = True
            `),console.log("[Worker] Setting up filesystem"),await this.pyodide.runPythonAsync(`
                import os
                os.makedirs('/project', exist_ok=True)
                os.chdir('/project')
            `),console.log("[Worker] Installing required packages"),await this.pyodide.loadPackage("micropip"),await this.pyodide.runPythonAsync(`
                import micropip
                await micropip.install('duckdb')
                await micropip.install('preswald')
                # await micropip.install("http://localhost:8000/preswald-0.1.54-py3-none-any.whl")
            `),console.log("[Worker] Initializing Preswald"),await this.pyodide.runPythonAsync(`
                import preswald.browser.entrypoint
            `),this.isInitialized=!0,console.log("[Worker] Initialization complete"),{success:!0}}catch(r){throw console.error("[Worker] Initialization error:",r),r}}async runScript(r){if(console.log("[Worker] Running script:",r),!this.isInitialized)throw new Error("Pyodide not initialized");try{this.activeScriptPath=r;const o=(await self.preswaldRunScript(r)).toJs();if(!o.success)throw new Error(o.error||"Script execution failed");const n=await this.pyodide.runPythonAsync(`
                import json
                from preswald.browser.virtual_service import VirtualPreswaldService
                service = VirtualPreswaldService.get_instance()
                components = service.get_rendered_components()
                json.dumps(components)
            `);return this.components=JSON.parse(n),{success:!0,components:this.components}}catch(t){throw console.error("[Worker] Script execution error:",t),t}}async updateComponent(r,t){if(console.log("[Worker] Updating component:",r,t),!this.isInitialized||!this.activeScriptPath)throw new Error("Not initialized or no active script");try{const n=(await self.preswaldUpdateComponent(r,t)).toJs();if(!n.success)throw new Error(n.error||"Component update failed");const i=await this.pyodide.runPythonAsync(`
                import json
                from preswald.browser.virtual_service import VirtualPreswaldService
                service = VirtualPreswaldService.get_instance()
                components = service.get_rendered_components()
                json.dumps(components)
            `);return this.components=JSON.parse(i),{success:!0,components:this.components}}catch(o){throw console.error("[Worker] Component update error:",o),o}}async loadFilesToFS(r){if(!this.pyodide)throw new Error("Pyodide not initialized");try{for(const[t,o]of Object.entries(r)){const n=t.substring(0,t.lastIndexOf("/"));n&&this.pyodide.runPython(`
                        import os
                        os.makedirs('${n}', exist_ok=True)
                    `),typeof o=="string"?this.pyodide.FS.writeFile(t,o):(o instanceof ArrayBuffer||ArrayBuffer.isView(o))&&this.pyodide.FS.writeFile(t,new Uint8Array(o))}return{success:!0}}catch(t){throw console.error("[Worker] File loading error:",t),t}}async clearFilesystem(){if(!this.pyodide)throw new Error("Pyodide not initialized");try{return await this.pyodide.runPythonAsync(`
                import os
                import shutil
                for item in os.listdir('/project'):
                    item_path = os.path.join('/project', item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
            `),{success:!0}}catch(r){throw console.error("[Worker] Filesystem clear error:",r),r}}async serializeFilesystem(){try{if(!this.pyodide)throw new Error("Pyodide not initialized");const r=await this.pyodide.runPythonAsync(`
                import os
                import json
                import base64
                
                def serialize_fs(root_dir='/project'):
                    result = {}
                    for root, dirs, files in os.walk(root_dir):
                        for file in files:
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, root_dir)
                            
                            try:
                                with open(full_path, 'r') as f:
                                  content = f.read()
                                result[rel_path] = {'type': 'text', 'content': content}
                            except UnicodeDecodeError:
                                with open(full_path, 'rb') as f:
                                  binary_content = f.read()
                                encoded = base64.b64encode(binary_content).decode('ascii')
                                result[rel_path] = {'type': 'binary', 'content': encoded}
                            
                    return result
                
                result_data = serialize_fs()
                json.dumps(result_data)
            `);return{success:!0,snapshot:JSON.parse(r)}}catch(r){throw console.error("[Worker] Filesystem serialization error:",r),r}}async getBrandingInfo(){try{if(!this.pyodide||!this.isInitialized)throw new Error("Pyodide not initialized");const r=self.PRESWALD_BRANDING;let t={};if(r&&typeof r=="string")try{t=JSON.parse(r)}catch(o){console.error("Error parsing branding JSON:",o)}return{success:!0,data:t}}catch(r){throw console.error("[Worker] Branding info error:",r),r}}async listFilesInDirectory(r){try{if(!this.pyodide||!this.isInitialized)throw new Error("Pyodide not initialized");const t=await this.pyodide.runPythonAsync(`
                import os
                import json
                
                result = {}
                try:
                    directory = "${r}"
                    files = os.listdir(directory)
                    result = files
                except Exception as e:
                    result = {"error": str(e)}
                
                json.dumps(result)
            `),o=JSON.parse(t);if(o&&o.error)throw new Error(o.error);return{success:!0,files:o}}catch(t){throw console.error("[Worker] Directory listing error:",t),t}}async shutdown(){if(this.pyodide&&this.isInitialized)try{await self.preswaldShutdown()}catch(r){console.error("Shutdown error:",r)}self.close()}}const $=new G;_($);
