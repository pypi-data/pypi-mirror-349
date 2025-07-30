<p align="center"> <img src="assets/neonize.png" width="150px">
</p>

## 

[![Release](https://github.com/krypton-byte/neonize/actions/workflows/release.yml/badge.svg)](https://github.com/krypton-byte/neonize/actions/workflows/release.yml)

<p align="justify">Neonize is a Python library designed to streamline the automation of tasks on WhatsApp. With neonize, users can easily automate various actions on WhatsApp, such as sending messages, processing received messages, and executing specific actions based on predefined scenarios.
</p>

**Key Features:**

1. **Message Automation:** Neonize provides a straightforward interface for sending automated messages to specific WhatsApp numbers.
2. **Message Processing:** Users can define functions or actions to be taken based on received messages. This allows users to create automated responses or run specific scenarios based on message content.
3. **Binding with <a href="https://github.com/tulir/whatsmeow">Whatsmeow</a>:** Neonize is built as a binding for the Whatsmeow library, leveraging similar functionality. This provides more flexibility in development and integration with functions that users may already be familiar with from Whatsmeow.
4. **Communication with Protobuf:** Neonize uses the Protobuf format as the communication protocol, offering speed and efficiency in data exchange between the application and WhatsApp.

**Usage:**

1. **Simple Installation:** Neonize can be easily installed through Python package managers such as pip.
   ```bash
   pip install neonize
   ```
2. **Initialization and Configuration:** Users can quickly configure neonize to use the desired WhatsApp account.
3. **Easy-to-Use:** Neonize provides a simple API and clear documentation to facilitate usage. Users can swiftly write scripts for WhatsApp automation according to their needs.

With neonize as a binding for Whatsmeow, WhatsApp automation becomes more accessible for Python developers, combining the strengths of both libraries and leveraging familiar functionalities from Whatsmeow.

To easily create a bot with minimal setup, you can utilize the <a href="https://github.com/krypton-byte/thundra">Thundra</a> library

## Contribution Guidelines

If you would like to contribute to this project, please follow these steps:

1. Fork this repository.
2. Create a new branch: `git checkout -b branch-name`.
3. Perform the desired tasks or changes.
4. Commit the changes: `git commit -m 'Commit message'`.
5. Push to branch: `git push origin branch-name`.
6. Send pull request.

## Local Development

If you want to run this project locally, follow these steps:

1. Clone the repository: `git clone git@github.com:krypton-byte/neonize.git`.
2. Install dependencies: `poetry install --with dev` (customize to the project).
3. Run the project: `python examples/basic.py` (customize to the project).

# Supported databases

Neonize currently supports `sqlite` and `postgres` database. Use postgres if you need a more performant database.

## Using Postgres as database store

Once you've created your postgres database, pass your full database url to the client. Database url will be in the format `"postgres://username:password@myhost:port/dbname"` e.g.

```python
client = NewAclient("postgres://username:password@myhost:port/dbname")
```

**Note:** You may need to enable or disable ssl mode depending.

```python
# Disable SSL mode
"postgres://username:password@myhost:port/dbname?sslmode=disable"

# Enable SSL Mode
"postgres://username:password@myhost:port/dbname?sslmode=verify-full"
```

## License

This project is licensed under Apache-2.0. See the [LICENSE](LICENSE) file for more information.

---
