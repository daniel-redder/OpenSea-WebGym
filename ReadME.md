# Welcome to OpenSea, a web interface for running multi-agent RL with the pettingzoo interface (and saving poor innocent grad students from needing to learn C++)

See Petting zoo documentation: [https://github.com/Farama-Foundation/PettingZoo](https://github.com/Farama-Foundation/PettingZoo)

We the authors of this paper \<> (for a research seminar nothing has been published) noticed that multi-agent RL (MARL) models are programmed in a variety of programming languages (python vs C++ vs dare I say it rust). The current MARL training paradigm is to train models with the same language. 

This makes sense from an easing perspective because each researcher has a set of domains they want to use which run their environments in a set language thus the models must follow. 

This leads to three problems:

1.  **Reproducibility:** By using language-specific environments and models it is challenging for any researcher skilled in only one popular language to reproduce the results of a model. 
2.  **Benchmarking:**
