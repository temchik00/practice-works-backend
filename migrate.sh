#!/bin/bash

echo "apply latest migrations"
alembic upgrade head
