# pyLeTalker - Wave-reflection voice synthesis framework (placeholder version)

`pyLeTalker` is a Python library to synthesize voice for research use, specifically aiming to enable the synethsis of pathologial voice. This library started as a repackaged version of [LeTalker, a Matlab GUI demo by Dr. Brad Story](https://sites.arizona.edu/sapl/research/le-talker/) but since has been evolved as a flexible general voice synthesis library built around the wave-reflection vocal tract model. The wave-reflection vocal tract model treats the vibrating air pressure as propagating waves through the vocal tract. Some portion of an incidental wave reflects when it encounters a change in the cross-sectional area of the vocal tract.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./docs_src/images/wave-reflection-model-dark.png">
  <img alt="Fallback image description" src="./docs_src/images/wave-reflection-model-light.png">
</picture>

The `pyLeTalker` modularize the voice production system into 5 elements: lung, subglottal tract, vocal folds (glottis), supraglottal tract, and lips. Each subsystem is implemented as a Python class. The library comes with one or more classes for each voice production element. For example, there are two built-in vocal-fold models: `LeTalkerVocalFolds` (self-oscillating 3-mass model with muscle activation inputs) and `KinematicVocalFolds` (3D vocal fold model with preprogrammed oscillation pattern).

The other part of `pyLeTalker` is its `function_generators` subpackage to enable time-varying control of voice production models. Actual voice production is perpetually dynamic. The synthesis models accept both constant parameter values as well as a `FunctionGenerator` object, so that the user can better program the behaviors.

Both synthesis elements and function generators can be customized. Hence, `pyLeTalker` is suitable framework to evaluate new vocal fold models.
