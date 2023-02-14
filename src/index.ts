import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  ICommandPalette,
} from '@jupyterlab/apputils';


import { requestAPI } from './handler';


function activate(app: JupyterFrontEnd, palette: ICommandPalette) {
  console.log('my plugin worksish');
  
  const command = 'cmd';
  app.commands.addCommand(command, {
    label: 'Model Test',
    execute: () => {
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
  });

  palette.addItem({command, category: 'Tutorial'});
}


const plugin: JupyterFrontEndPlugin<void> = {
  id: 'model_test',
  autoStart: true,
  requires: [ICommandPalette],
  activate: activate
};


export default plugin;