# Customer Success API Reference

## Internal CSM Endpoints (`/api/v1/customer-success`)

* `POST /profiles`: Upsert client success profile.
* `GET /profiles`: List client success profiles with lifecycle filtering.
* `GET /profiles/{client_id}`: Get specific client profile.
* `POST /relationships`: Register stakeholder relationship.
* `GET /relationships/{client_id}`: List client stakeholders.
* `POST /timeline`: Log cross-module timeline event.
* `GET /timeline/{client_id}`: Retrieve chronological activity stream.
* `POST /goals`: Register strategic client goal.
* `GET /goals/{client_id}`: List client goals.
* `POST /health/calculate`: Compute pure mathematical health score without persisting.
* `POST /health/{client_id}/record`: Calculate and record health snapshot & history.
* `GET /health/{client_id}/latest`: Get most recent health score.
* `GET /health/{client_id}/history`: Retrieve historical score trend data.
* `POST /risks`: Log client risk item.
* `GET /risks`: List active risks.
* `POST /opportunities`: Register expansion opportunity candidate.
* `GET /opportunities`: List active opportunities.
* `POST /renewals`: Schedule contract renewal cycle.
* `GET /renewals`: List upcoming renewals.
* `GET /clients/{client_id}/360`: Synthesize comprehensive 360-degree client dossier.

## Client Portal Endpoints (`/api/v1/portal/success`)

* `GET /overview`: Retrieve masked 360 overview (internal risks & margins scrubbed).
* `GET /goals`: Retrieve client-visible shared goals.
* `GET /timeline`: Retrieve client-visible milestones and announcements.
* `POST /surveys/submit`: Submit CSAT/NPS survey response.
