# Template Python Project 

Template for a Fast API project. This template is based on the
[python_project_template](https://github.com/STRAST-UPM/python_project_template)
from STRAST research group that can be found in the same organization as this 
one. The same structure of files and folder applies, check the original for more
detailed information.

## Project Structure

This section describe the updates made to the base template to fit FastAPI
properly.

### Files and folders updates

- `code/src/classes/routers` is the package used to keep the routers that
control the different main endpoints.

## Deployment on containers

As it was told this project was though to be used with containers for easy
deployment. The base containers deployed are the project developed and a
PostgreSQL database with a web administration console accesible. The following
URL is for the [FastAPI Docs](http://localhost) and the second one for the
[Postgres admin console](http://localhost:8080). The database and administration
console have permanent storage via Docker volumes.

- Build project image
```shell
sudo docker build -t user/fastapi_template:latest .
```

- Push image to repository
```shell
sudo docker push user/fastapi_template:latest
```

- Run project just project container
```shell
sudo docker run \
  -p "8000:8000" \
  --name fastapi_template \
  -d user/fastapi_template:latest
```

- Start deployment
```shell
sudo docker compose up -d
```

---

Developed by the research group Sistemas de Tiempo Real y Arquitectura de
Sistemas Telemáticos (STRAST) part of Departamento de Ingeniería de Sistemas
Telemáticos (DIT) located in Escuela Técnica Superior de Ingenieros de
Telecomunicación (ETSIT) part of Universidad Politécnica de Madrid
department (UPM).

**Contact**
- gi.strast@upm.es
- [Web page](http://web.dit.upm.es/~str/)
- [GitHub](https://github.com/STRAST-UPM/)

<img alt="logo_dit" src="./docu/statics/dit_logo.gif" width="80"/>

![upm_logo](./docu/statics/upm_logo.png)

---

LICENSE

This software is licensed under Creative Common
Attribution-NonCommercial-ShareAlike 4.0 International. You may not use this
software except in compliance with this license.

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

fastapi_template © 2025 by STRAST is licensed under Creative Commons
Attribution-NonCommercial-ShareAlike 4.0 International.
