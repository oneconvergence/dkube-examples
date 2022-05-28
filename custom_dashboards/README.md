This folder describes how to embed dashboards created on external Tableau, Grafana like services in iframes and render on monitor details page. 

### Sample Dashboard

DKube provides a default alert dashboard using grafana. This can be rendered as one of the tabs on Monitor details page. 

- Download and edit [alerts.json](alerts.json) file and replace the following
-- <DKube-UI-IP:32222> with IP address and Port of DKube UI server
-- <MONITOR-ID> with the monitor ID for the specific deployment
- Goto the list view of the monitors and click on 'Update Dashboard' Action for the monitor of your choice and upload the updated json file.

### More Advanced Dashboards
The above example creates a single new tab. However, you could have 1 or more top level tabs, and 1 or more 2nd level tabs or pages in each top level tab. This can be achieved by downloading [business_metrics.json](business_metrics.json) and following the instructions in the json file. After you update, upload the file in the same manner as described above.

A sample file with a 2 level hierarchy of tabs has been created using public URLs. [random_public_urls.json](random_public_urls.json) can be uploaded as such without any changes. 


**Note**: If you are importing **tableau** dashboards, please include the substring *&:showVizHome=no&:embed=true*

