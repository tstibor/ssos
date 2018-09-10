#!/usr/bin/env python3
'''
  Pipeline to search for Solar System objects in wide-field imaging surveys
  Information on the project can be found in arXiv:1711.02780

  For questions, contact max.mahlke (at) cab.inta-csic.es

  Max Mahlke, August 2018
'''

import os

from core import Pipeline


def main():
    # ========
    # Start the pipeline.  This step initializes the log, the target directory,
    # evaluates and checks the pipeline settings and verifies the input images.
    # ========
    pipeline = Pipeline()

    # ------
    # Run SExtractor on images
    pipeline.log.info('\nRunning SExtractor..\t')
    pipeline.run_SExtractor()

    # ------
    # Run SCAMP on SExtractor catalogues
    pipeline.log.info('\nRunning SCAMP..\t')
    pipeline.run_SCAMP()

    # ========
    # Catalogue creation done
    # ========

    pipeline.log.info('\n --- Starting Filter pipeline ---\n\n')
    pipeline.log.info('%s %i\n' % ('All Sources'.ljust(20), pipeline.number_of_sources()))

    # Call pipeline filter steps
    for step in pipeline.steps:
        pipeline.execute_filter(step)
        pipeline.log.info('%s %i \n' % (step.ljust(20), pipeline.number_of_sources()))

    if not pipeline.added_proper_motion:
        pipeline.add_proper_motion()

    if not pipeline.added_trail_morphology:
        pipeline.add_trail_morphology()

    # ========
    # FILTERING COMPLETE
    # ========

    # ------
    # Optional analyses
    for step in pipeline.analysis_steps:
        pipeline.execute_analysis(step)

    # ------
    # Rename columns, remove unnecessary data, save to file
    pipeline.save_and_cleanup()

    pipeline.log.info('\t|\t'.join(
                     ['\nAll done!',
                      '%i SSO candidates found' % pipeline.number_of_sources(),
                      'The analysis ran in %i seconds\n\n' % pipeline.run_time]))

    pipeline.log.info('Output File: %s\nLog File: %s\n\n' %
                     (os.path.join(pipeline.paths['cats'], 'ssos.csv'),
                      os.path.join(pipeline.paths['logs'], pipeline.log_file)))


if __name__ == '__main__':
    main()