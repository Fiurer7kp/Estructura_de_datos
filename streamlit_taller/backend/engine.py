"""
CI/CD Simulator - Pipeline Engine
Autor: Sebastian Coral | Ing. de Software
"""
import random, time
from .data_structures import EXECUTION_AGENTS, PipelineLinkedList, JobQueue, DeploymentStack, LogViewer

class CICDEngine:
    _ver = [1, 0, 0]

    def __init__(self):
        self.agents       = [a.copy() for a in EXECUTION_AGENTS]
        self.pipeline     = PipelineLinkedList()
        self.job_queue    = JobQueue()
        self.deploy_stack = DeploymentStack()
        self.logs         = LogViewer()
        self.logs.add("Sistema CI/CD inicializado", "INFO", "engine")

    # Agents
    def _free_agent(self):  return next((a for a in self.agents if a["status"] == "idle"), None)
    def _set_agent(self, i, s): self.agents[i]["status"] = s

    # Jobs
    def submit_job(self, developer, branch):
        job = self.job_queue.enqueue(developer, branch)
        self.logs.add(f"Job {job['id']} encolado por {developer} [{branch}]", "INFO", developer)
        return job

    # Pipeline execution
    def run_pipeline(self):
        events = []
        job = self.job_queue.dequeue()
        if not job:
            self.logs.add("No hay jobs en cola", "WARNING", "engine"); return events

        agent = self._free_agent()
        if not agent:
            self.logs.add("Sin agentes libres, re-encolando...", "WARNING", "engine")
            self.job_queue._q.appendleft(job); return events

        self._set_agent(agent["id"], "busy")
        self.pipeline.reset()
        self.logs.add(f"Iniciando {job['id']} en {agent['name']}", "INFO", "engine")
        events.append({"type": "start", "job": job, "agent": agent})

        success = True
        for stage in self.pipeline.to_list():
            stage.status = "running"
            self.logs.add(f"▶ Stage: {stage.name}", "INFO", stage.name)
            time.sleep(0.05)

            if random.random() < 0.15:
                stage.status = "failed"
                self.logs.add(f"Falló: {stage.name}", "ERROR", stage.name)
                events.append({"type": "stage_fail", "stage": stage.name})
                success = False; break
            else:
                stage.status = "success"
                self.logs.add(f"Completado: {stage.name}", "SUCCESS", stage.name)
                events.append({"type": "stage_ok", "stage": stage.name})

        self._set_agent(agent["id"], "idle")

        if success:
            ver = self._next_version()
            self.deploy_stack.push(ver, job["id"])
            self.logs.add(f"Desplegado {ver}", "SUCCESS", "deploy")
            events.append({"type": "deployed", "version": ver})
        else:
            self.logs.add("Pipeline fallido", "ERROR", "engine")
            events.append({"type": "pipeline_failed"})

        return events

    # Rollback
    def emergency_rollback(self):
        removed, restored = self.deploy_stack.rollback()
        if removed:
            self.logs.add(f"ROLLBACK: {removed['version']} → {restored['version']}", "WARNING", "rollback")
        else:
            self.logs.add("Sin versión anterior disponible", "WARNING", "rollback")
        return removed, restored

    def _next_version(self):
        self._ver[2] += 1
        if self._ver[2] >= 10: self._ver[2] = 0; self._ver[1] += 1
        return "v" + ".".join(map(str, self._ver))
