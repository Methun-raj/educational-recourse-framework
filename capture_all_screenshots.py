"""
Automated High-Resolution Screenshot Capture Engine for EduForecaster XAI
Uses Edge/Chromium Chrome DevTools Protocol (CDP) to interact with the running web application,
execute presets, run hierarchical cascade inference, apply recourse, and save clean PNG screenshots.
"""

import subprocess
import time
import json
import urllib.request
import asyncio
import websockets
import base64
import os
import sys

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

msg_id = 0

async def send_cmd(ws, method, params=None):
    global msg_id
    msg_id += 1
    cid = msg_id
    payload = {"id": cid, "method": method, "params": params or {}}
    await ws.send(json.dumps(payload))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == cid:
            return data.get("result", {})

async def eval_js(ws, expr):
    res = await send_cmd(ws, "Runtime.evaluate", {
        "expression": expr,
        "awaitPromise": True,
        "returnByValue": True
    })
    return res.get("result", {}).get("value")

async def wait_for_condition(ws, js_condition, timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        val = await eval_js(ws, js_condition)
        if val:
            return True
        await asyncio.sleep(0.3)
    return False

async def capture_screenshot(ws, filename, full_page=False):
    out_path = os.path.join(OUTPUT_DIR, filename)
    params = {"format": "png"}
    if full_page:
        # Get layout metrics
        metrics = await send_cmd(ws, "Page.getLayoutMetrics")
        content_size = metrics.get("contentSize", {})
        width = int(content_size.get("width", 1440))
        height = int(content_size.get("height", 900))
        # Set device metrics override
        await send_cmd(ws, "Emulation.setDeviceMetricsOverride", {
            "width": width,
            "height": height,
            "deviceScaleFactor": 1,
            "mobile": False
        })
        params["captureBeyondViewport"] = True
    
    shot = await send_cmd(ws, "Page.captureScreenshot", params)
    data = base64.b64decode(shot["data"])
    with open(out_path, "wb") as f:
        f.write(data)
    
    # Reset device metrics if full_page was set
    if full_page:
        await send_cmd(ws, "Emulation.clearDeviceMetricsOverride")

    size_kb = len(data) / 1024
    print(f"Captured: {filename} ({size_kb:.1f} KB)")
    return out_path

async def run_capture():
    profile_dir = os.path.join(os.environ["TEMP"], "edge_screenshot_cdp")
    os.makedirs(profile_dir, exist_ok=True)

    print("Launching Edge Headless with CDP on port 9222...")
    proc = subprocess.Popen([
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--remote-debugging-port=9222",
        f"--user-data-dir={profile_dir}",
        "--window-size=1440,1000"
    ])

    try:
        time.sleep(2)
        tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json").read().decode())
        ws_url = None
        for t in tabs:
            if t.get("type") == "page":
                ws_url = t.get("webSocketDebuggerUrl")
                break
        if not ws_url:
            ws_url = tabs[0]["webSocketDebuggerUrl"]

        print(f"Connecting to CDP: {ws_url}")
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            await send_cmd(ws, "Page.enable")
            await send_cmd(ws, "Runtime.enable")
            await send_cmd(ws, "DOM.enable")

            # -------------------------------------------------------------
            # 1. Main Dashboard: Home & Architecture Banner
            # -------------------------------------------------------------
            print("\n1. Navigating to Main Dashboard (Home)...")
            await send_cmd(ws, "Page.navigate", {"url": "http://127.0.0.1:5000/"})
            await asyncio.sleep(2)
            await capture_screenshot(ws, "01_dashboard_home.png")

            # -------------------------------------------------------------
            # 2. Run Cascaded Prediction for Canonical At-Risk Student
            # -------------------------------------------------------------
            print("\n2. Executing At-Risk Student Prediction...")
            await eval_js(ws, "loadPreset('at_risk');")
            await asyncio.sleep(0.5)
            await eval_js(ws, "handleFormSubmit();")
            # Wait for results container to appear
            await wait_for_condition(ws, "document.getElementById('results-container').style.display !== 'none'")
            await asyncio.sleep(1.5)  # allow charts to render smoothly

            # Scroll to results banner and charts
            await eval_js(ws, "document.getElementById('results-container').scrollIntoView({ behavior: 'instant' });")
            await asyncio.sleep(0.5)
            await capture_screenshot(ws, "02_at_risk_forecast_and_shap.png")

            # -------------------------------------------------------------
            # 3. Actionable Counterfactual Recourse Section
            # -------------------------------------------------------------
            print("\n3. Capturing Actionable Counterfactual Recourse Plan...")
            await eval_js(ws, "document.getElementById('recourse-section').scrollIntoView({ behavior: 'instant' });")
            await asyncio.sleep(0.5)
            await capture_screenshot(ws, "03_counterfactual_recourse_plan.png")

            # -------------------------------------------------------------
            # 4. Apply Counterfactual Recourse & Re-Forecast (Placement Achieved)
            # -------------------------------------------------------------
            print("\n4. Applying Recourse & Re-Forecasting (Probability: 91.0%)...")
            await eval_js(ws, "applyCounterfactualRecourse();")
            await asyncio.sleep(1.5)
            await eval_js(ws, "document.getElementById('results-container').scrollIntoView({ behavior: 'instant' });")
            await asyncio.sleep(0.5)
            await capture_screenshot(ws, "04_recourse_reforecast_success.png")

            # -------------------------------------------------------------
            # 5. Scientific Research Benchmarks Page
            # -------------------------------------------------------------
            print("\n5. Navigating to Scientific Research Benchmarks Page...")
            await send_cmd(ws, "Page.navigate", {"url": "http://127.0.0.1:5000/benchmarks"})
            await asyncio.sleep(2)
            await capture_screenshot(ws, "05_research_benchmarks_overview.png")

            # Scroll to benchmark tables and calibration figure
            await eval_js(ws, "window.scrollTo(0, 750);")
            await asyncio.sleep(0.5)
            await capture_screenshot(ws, "06_calibration_and_metrics.png")

            # -------------------------------------------------------------
            # 6. Datasets Explorer Page & User Integration Form
            # -------------------------------------------------------------
            print("\n6. Navigating to Datasets Explorer Page...")
            await send_cmd(ws, "Page.navigate", {"url": "http://127.0.0.1:5000/datasets"})
            await asyncio.sleep(2)
            await capture_screenshot(ws, "07_datasets_explorer.png")

            # Scroll down to dynamic user data integration form
            await eval_js(ws, "document.getElementById('integration-form-card').scrollIntoView({ behavior: 'instant' });")
            await asyncio.sleep(0.5)
            await capture_screenshot(ws, "08_user_data_integration_form.png")

            print("\nAll 8 high-resolution screenshots captured successfully!")

    finally:
        proc.terminate()
        print("Edge CDP process terminated.")

if __name__ == "__main__":
    asyncio.run(run_capture())
