/**
 * UnitML
 * Copyright 2023 Carnegie Mellon University.
 * NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.
 * Released under a BSD (SEI)-style license, please see license.txt or contact permission@sei.cmu.edu for full terms.
 * [DISTRIBUTION STATEMENT A] This material has been approved for public release and unlimited distribution.  Please see Copyright notice for non-US Government use and distribution.
 * This Software includes and/or makes use of Third-Party Software each subject to its own license.
 * DM23-0976
 */


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
    label: 'UnitML',
    execute: () => {
      requestAPI<any>('get_example')
        .then(data => {
          console.log(data);
        })
        .catch(reason => {
          console.error(
            `The unitml server extension ran into an error.\n${reason}`
          );
        });
    }
  });

  palette.addItem({command, category: 'Tutorial'});
}


const plugin: JupyterFrontEndPlugin<void> = {
  id: 'unitml',
  autoStart: true,
  requires: [ICommandPalette],
  activate: activate
};


export default plugin;