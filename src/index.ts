import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

/**
 * Initialization data for the model_test extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'model_test:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension model_test is activated!');

    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The model_test server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
