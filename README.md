# Flask Prometheus Monitoring Example

This project demonstrates a basic Flask web application integrated with Prometheus for exposing application metrics. It showcases the usage of different Prometheus metric types: `Counter`, `Gauge`, and `Histogram`, to monitor various aspects of the application's performance and usage.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
- [Running the Application](#running-the-application)
- [Application Endpoints](#application-endpoints)
- [Prometheus Metrics Explained](#prometheus-metrics-explained)
  - [`Counter`](#counter)
  - [`Gauge`](#gauge)
  - [`Histogram`](#histogram)
- [How to View Metrics](#how-to-view-metrics)
- [Contribution](#contribution)
- [License](#license)

---

## Project Overview

This is a minimal Flask application designed to illustrate how to instrument a Python web service with Prometheus client library. It exposes a `/metrics` endpoint that Prometheus servers can scrape to collect time-series data about the application's behavior, such as total requests, in-progress requests, and request latency.

## Features

* **Simple Flask Application:** A straightforward Flask app with a home page and a simulated "slow" endpoint.
* **Prometheus Metric Integration:** Demonstrates the use of:
    * `Counter`: To track the total number of requests to specific endpoints.
    * `Gauge`: To monitor the number of concurrent, in-progress requests.
    * `Histogram`: To observe and bucket request durations, providing insights into latency distribution.
* **`/metrics` Endpoint:** A dedicated endpoint that serves Prometheus-formatted metrics, ready for scraping.

## Prerequisites

Before you begin, ensure you have the following installed on your Fedora system (or any Linux distribution):

* **Python 3.x:** The application is written in Python.
* **`pip`:** Python's package installer, usually comes with Python.
* **`venv` module:** For creating isolated Python environments.

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository

First, clone this repository to your local machine. If this code is part of a larger project, navigate to your project's root directory.

```bash
git clone <your-repository-url>
cd <your-project-directory> # e.g., cd flask-prometheus-example