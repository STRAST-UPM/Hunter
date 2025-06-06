# Hunter

Network tool specialized on anycast IP destination tracking. 

## Deployment 

For building the image and push it to the remote repository you can use 
`build_and_push.sh` script or the following commands.

- Build project image
```shell
sudo docker build -t strast-upm/hunter:latest .
```

- Push image to repository
```shell
sudo docker tag strast-upm/hunter:latest ghcr.io/strast-upm/hunter:latest
sudo docker push ghcr.io/strast-upm/hunter:latest
```

- Run project just project container
```shell
sudo docker run \
  -p "80:8000" \
  --name hunter \
  -d strast-upm/hunter:latest
```

- Start deployment
```shell
sudo docker compose up -d
```

### Web browser interfaces

- [Hunter Swagger](http://localhost/docs)
- [Postgres admin console](http://localhost:8080)

## Related publications

- Hugo Pascual, Jose M. del Alamo, David Rodriguez, Juan C. Dueñas,
Hunter: Tracing anycast communications to uncover cross-border personal data transfers,
Computers & Security, Volume 141, 2024, 103823, ISSN 0167-4048,
https://doi.org/10.1016/j.cose.2024.103823.

- H. Pascual, J. M. D. Alamo, D. Rodriguez and J. C. Duenas,
"Anycast and Third-party Libraries: A Recipe for a Privacy Disaster?," in 
IEEE Communications Magazine, https://doi.org/10.1109/MCOM.006.2400576.

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
