#!/usr/bin/env python
import os
import math
import pickle

class Session:
    def __init__(self, path):
        self.config_file = "session.conf"
        self.path = path
        self.load(path)

    def load(self, path):
        conf_path = self.path + "/" + self.config_file
        if os.path.isfile(conf_path):
            config = {}
            with open(conf_path, "r") as f:
                config = pickle.load(f) 

            self.configuration = config
            return True
        else:
            return False

    def save(self):
        conf_path = self.path + "/" + self.config_file
        with open(conf_path, "w") as f:
            pickle.dump(self.configuration, f) 
        return True

    def create(self, config, args):
        self.configuration = {}
        self.configuration["command"] = args["command"]
        self.configuration["batch_size"] = args["batch_size"]
        self.configuration["read"] = args["read"]
    
        self.configuration["stdout_file"] = config["session_stdout_file"]
        self.configuration["stderr_file"] = config["session_stderr_file"]
        self.configuration["status_file"] = config["session_status_file"]

        with open(self.path + "/" + self.configuration["stdout_file"], "w") as f:
            f.write("")
        with open(self.path + "/" + self.configuration["stderr_file"], "w") as f:
            f.write("")
        with open(self.path + "/" + self.configuration["status_file"], "w") as f:
            f.write("")

        self.save()
    
    def get_batches(self):
        all_batches = os.listdir(self.path)
        all_batches = filter(lambda x: os.path.isfile(self.path + "/" + x), all_batches)
        all_batches = filter(lambda x: os.path.splitext(self.path + "/" + x)[1] == ".batch", all_batches)
        return all_batches

    def get_incomplete_batches(self):
        all_batches = self.get_batches()

        with open(self.path + "/" + self.configuration["status_file"], "r") as f:
            completed_batches = map(lambda x: x.strip(), f.readlines())
        
        return [ batch for batch in all_batches if batch not in completed_batches ]

    def get_stdout(self):
        data = ""
        with open(self.path + "/" + self.configuration["stdout_file"], "r") as f:
            data = "\n".join(map(lambda x: x.strip(), f.readlines()))
        return data

    def get_stderr(self):
        data = ""
        with open(self.path + "/" + self.configuration["stderr_file"], "r") as f:
            data = "\n".join(map(lambda x: x.strip(), f.readlines()))
        return data

    def get_batch(self, batch):
        data = ""
        with open(self.path + "/" + batch, "r") as f:
            data = "\n".join(map(lambda x: x.strip(), f.readlines()))
        return data

    def save_status(self, batch, stdout, stderr):
        with open(self.path + "/" + self.configuration["status_file"], "a") as f:
            f.write(batch + "\n")
        with open(self.path + "/" + self.configuration["stdout_file"], "a") as f:
            f.write(stdout)
        with open(self.path + "/" + self.configuration["stderr_file"], "a") as f:
            f.write(stderr)

    def generate_batches(self, jobstream):
        # TODO: Improvement would be to not read everything into memory
        jobs = map(lambda x: x.strip(), jobstream.readlines())

        batch_size = self.configuration["batch_size"]
        number_batches = int(math.ceil(len(jobs) / float(batch_size)))
        number_jobs = len(jobs)

        batches = []
        job_offset = 0
        for i in range(0, number_batches):
            batch = []
            job_offset = i * batch_size
            for c in range(0, batch_size):
                if c + job_offset >= number_jobs:
                    break
                batch.append(jobs[c+job_offset])
            batches.append(batch)

        for i in range(0, len(batches)):
            batch_name = "%d.batch" % i
            with open(self.path + "/" + batch_name, "w") as f:
                for job in batches[i]:
                    f.write(job + "\n")
