# ContextIQ — Demo Video Shotlist & Manual Screen Recording Guide

**Target Video Duration**: 60 – 120 seconds  
**Recommended Screen Resolution**: 1920x1080 (1080p, 60fps)

---

## Shotlist Breakdown

| Timecode | Screen / View | Action / Script |
|---|---|---|
| **00:00 – 00:10** | **Executive Dashboard (`/`)** | Open React Studio UI. Point out enterprise statistics (50 Machines, 150 Sensors, 182 Document Chunks) and live health indicators. |
| **00:10 – 00:30** | **Knowledge Graph (`/graph`)** | Navigate to Knowledge Graph visualizer. Expand node `M001`, show relationships to `DOC-031` and `B101`. |
| **00:30 – 00:55** | **AI Copilot (`/copilot`)** | Type Scenario 1 query: *"What maintenance procedure applies to machine M001 and what is the lubrication interval for spindle bearing B101?"* |
| **00:55 – 01:20** | **Copilot Response & Citations** | Highlight grounded answer, document evidence cards, citation tags (`DOC-031`), and Neo4j graph context path. |
| **01:20 – 01:45** | **AI Benchmark Center (`/evaluation`)** | Navigate to Evaluation page. Showcase official metrics: P@1 (26.7%), R@3 (40.0%), MRR (33.2%), Groundedness (100.0%), and 30 test cases. |
| **01:45 – 02:00** | **System Health & Terminal (`/system`)** | Show green API readiness status and terminal running 148 passing Pytest tests. |

---

## Manual Recording Steps (OBS Studio / Screen Recorder)

1. **Start Backend**: `uvicorn api.main:app --port 8000`
2. **Start Frontend**: `cd frontend && npm run dev`
3. Open browser at `http://localhost:5173`
4. Record screen following the timecode shotlist above.
5. Export as MP4 or GIF (`assets/demo/contextiq-demo.gif`).
