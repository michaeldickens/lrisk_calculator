from functools import cache
import html
import pdb

from pydtmc import MarkovChain


# This script prints out a series of probabilities for transition becoming interstellar based on
# estimates of the transition probabilities of various(values are currently hardcoded placeholders)
# states, as in a Markov chain. The states are extinction, pre_equilibrium, preindustrial, industrial, time
# of perils, multiplanetary, and interstellar.
#
# A full description/explanation of the model is in the section titled The Cyclical Model in this
# post:
# https://forum.effectivealtruism.org/posts/YnBwoNNqe6knBJH8p/modelling-civilisation-after-a-catastrophe#The_cyclical_model
#
# These values are all placeholders. Add your own, and see what happens.

# TODO Might want this model to still have two ToP-states - the current one, and all future ones

# Transition probabilities


class SimpleCalc:
  def __init__(self, form):
    self.form = form

  # From pre-equilibrium

  def extinction_given_pre_equilibrium(self):
    return float(self.form['extinction_given_pre_equilibrium'])

  def preindustrial_given_pre_equilibrium(self):
    return 1 - self.extinction_given_pre_equilibrium()


  # From preindustrial

  def extinction_given_preindustrial(self):
    return float(self.form['extinction_given_preindustrial'])

  def industrial_given_preindustrial(self):
    return 1 - self.extinction_given_preindustrial()


  # From industrial

  def extinction_given_industrial(self):
    return float(self.form['extinction_given_industrial'])

  def future_perils_given_industrial(self):
    return 1 - self.extinction_given_industrial()


  # From present perils

  def extinction_given_present_perils(self):
    return float(self.form['extinction_given_present_perils'])

  def pre_equilibrium_given_present_perils(self):
    return float(self.form['pre_equilibrium_given_present_perils'])

  def preindustrial_given_present_perils(self):
    return float(self.form['preindustrial_given_present_perils'])

  def industrial_given_present_perils(self):
    return float(self.form['industrial_given_present_perils'])

  def future_perils_given_present_perils(self):
    return float(self.form['future_perils_given_present_perils'])

  def interstellar_given_present_perils(self):
    return float(self.form['interstellar_given_present_perils'])

  def multiplanetary_given_present_perils(self):
    return 1 - (self.extinction_given_present_perils()
                + self.pre_equilibrium_given_present_perils()
                + self.preindustrial_given_present_perils()
                + self.industrial_given_present_perils()
                + self.future_perils_given_present_perils()
                + self.interstellar_given_present_perils())


  # From future perils

  def extinction_given_future_perils(self):
    return float(self.form['extinction_given_future_perils'])

  def pre_equilibrium_given_future_perils(self):
    return float(self.form['pre_equilibrium_given_future_perils'])

  def preindustrial_given_future_perils(self):
    return float(self.form['preindustrial_given_future_perils'])

  def industrial_given_future_perils(self):
    return float(self.form['industrial_given_future_perils'])

  def interstellar_given_future_perils(self):
    return float(self.form['interstellar_given_future_perils'])

  def multiplanetary_given_future_perils(self):
    return 1 - (self.extinction_given_future_perils()
                + self.pre_equilibrium_given_future_perils()
                + self.preindustrial_given_future_perils()
                + self.industrial_given_future_perils()
                + self.interstellar_given_future_perils())


  # From mutiplanetary

  def extinction_given_multiplanetary(self):
    return float(self.form['extinction_given_multiplanetary'])

  def pre_equilibrium_given_multiplanetary(self):
    return float(self.form['pre_equilibrium_given_multiplanetary'])

  def preindustrial_given_multiplanetary(self):
    return float(self.form['preindustrial_given_multiplanetary'])

  def industrial_given_multiplanetary(self):
    return float(self.form['industrial_given_multiplanetary'])

  def future_perils_given_multiplanetary(self):
    return float(self.form['future_perils_given_multiplanetary'])

  def interstellar_given_multiplanetary(self):
    return 1 - (self.extinction_given_multiplanetary()
                + self.pre_equilibrium_given_multiplanetary()
                + self.preindustrial_given_multiplanetary()
                + self.industrial_given_multiplanetary()
                + self.future_perils_given_multiplanetary())

  @cache
  def markov_chain(self):
    extinction_transition_probabilities =     [1, 0, 0, 0, 0, 0, 0, 0]
    pre_equilibrium_transition_probabilities =       [self.extinction_given_pre_equilibrium(),
                                               0,
                                               self.preindustrial_given_pre_equilibrium(),
                                               0,
                                               0,
                                               0,
                                               0,
                                               0]
    preindustrial_transition_probabilities =  [self.extinction_given_preindustrial(),
                                               0,
                                               0,
                                               self.industrial_given_preindustrial(),
                                               0,
                                               0,
                                               0,
                                               0]
    industrial_transition_probabilities =     [self.extinction_given_industrial(),
                                               0,
                                               0,
                                               0,
                                               0,
                                               self.future_perils_given_industrial(),
                                               0,
                                               0]
    present_perils_transition_probabilities = [self.extinction_given_present_perils(),
                                               self.pre_equilibrium_given_present_perils(),
                                               self.preindustrial_given_present_perils(),
                                               self.industrial_given_present_perils(),
                                               0,
                                               self.future_perils_given_present_perils(),
                                               self.multiplanetary_given_present_perils(),
                                               self.interstellar_given_present_perils()]
    future_perils_transition_probabilities =   [self.extinction_given_future_perils(),
                                               self.pre_equilibrium_given_future_perils(),
                                               self.preindustrial_given_future_perils(),
                                               self.industrial_given_future_perils(),
                                               0,
                                               0,
                                               self.multiplanetary_given_future_perils(),
                                               self.interstellar_given_future_perils()]
    multiplanetary_transition_probabilities = [self.extinction_given_multiplanetary(),
                                               self.pre_equilibrium_given_multiplanetary(),
                                               self.preindustrial_given_multiplanetary(),
                                               self.industrial_given_multiplanetary(),
                                               0,
                                               self.future_perils_given_multiplanetary(),
                                               0,
                                               self.interstellar_given_multiplanetary()]
    interstellar_transition_probabilities =   [0, 0, 0, 0, 0, 0, 0, 1]

    transition_probability_matrix = [extinction_transition_probabilities,
                                     pre_equilibrium_transition_probabilities,
                                     preindustrial_transition_probabilities,
                                     industrial_transition_probabilities,
                                     present_perils_transition_probabilities,
                                     future_perils_transition_probabilities,
                                     multiplanetary_transition_probabilities,
                                     interstellar_transition_probabilities]

    # mini = [[0.2, 0.7, 0.0, 0.1], [0.0, 0.6, 0.3, 0.1], [0.0, 0.0, 1.0, 0.0], [0.5, 0.0, 0.5, 0.0]]
    # mc = MarkovChain(mini, ['A', 'B', 'C', 'D'])

    return MarkovChain(transition_probability_matrix, ['Extinction',
                                                       'Pre-equilibrium',
                                                       'Preindustrial',
                                                       'Industrial',
                                                       'Present perils',
                                                       'Future perils',
                                                       'Multiplanetary',
                                                       'Interstellar'])

    # Shortcuts for the probability of direct-path transitions

  def probability_of_preindustrial_to_perils_directly(self):
    return self.industrial_given_preindustrial() * self.future_perils_given_industrial()

  def probability_of_pre_equilibrium_to_perils_directly(self):
    return self.preindustrial_given_pre_equilibrium() * self.probability_of_preindustrial_to_perils_directly()

  def net_interstellar_from_pre_equilibrium(self):
    return self.markov_chain().absorption_probabilities()[1][0]

  def net_interstellar_from_preindustrial(self):
    return self.markov_chain().absorption_probabilities()[1][1]

  def net_interstellar_from_industrial(self):
    return self.markov_chain().absorption_probabilities()[1][2]

  def net_interstellar_from_perils(self):
    return self.markov_chain().absorption_probabilities()[1][3]

  def net_interstellar_from_multiplanetary(self):
    return self.markov_chain().absorption_probabilities()[1][4]

  def total_probability_of_non_extinction_milestone_regression_from_perils(self):
    return self.pre_equilibrium_given_perils() + self.preindustrial_given_perils() + self.industrial_given_perils()

  # def weighted_net_interstellar_from_unspecified_regress(self):
  #   return ((self.net_interstellar_from_pre_equilibrium() * self.pre_equilibrium_given_perils())
  #            + (self.net_interstellar_from_preindustrial() * self.preindustrial_given_perils())
  #            + (self.net_interstellar_from_industrial() * self.industrial_given_perils())
  #               / self.total_probability_of_non_extinction_milestone_regression_from_perils())

  def pre_equilibrium_probability_reduction(self):
    return str((self.net_interstellar_from_perils() - self.net_interstellar_from_pre_equilibrium())
                / self.net_interstellar_from_perils() * 100) + '%'

  def preindustrial_probability_reduction(self):
    return str((self.net_interstellar_from_perils() - self.net_interstellar_from_preindustrial())
                / self.net_interstellar_from_perils() * 100) + '%'

  def industrial_probability_reduction(self):
    return str((self.net_interstellar_from_perils() - self.net_interstellar_from_industrial())
               / self.net_interstellar_from_perils() * 100) + '%'

  def multiplanetary_probability_increase(self):
    return str((self.net_interstellar_from_multiplanetary() - self.net_interstellar_from_perils())
                / self.net_interstellar_from_perils() * 100) + '%'




















