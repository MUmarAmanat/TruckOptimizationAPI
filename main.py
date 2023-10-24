"""FastAPI main file for implementation of maximize truck capacity."""
import json
from typing import List
from solver import Solver
from pulp import *
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Input(BaseModel):
    """Class representing input parameters"""
    numberOfProducts: int
    numberOfTruckTypes: int
    productVolumes: List[float]
    productDemandQuantity: List[int]
    truckTypeCapacities: List[int]
    numberOfTrucksPerType: List[int]


@app.get("/")
def home_page():
    """
    Description: Homepage function
    Parameters: None
    Return: Message (String)
    """
    return "Welcome! Perform a POST request on /run/ path. Or enter http://<public-ip:port>/docs"

@app.post("/run/")
def call_funct(input: Input):
    """
    Description: Main function to solve LP Problem
    Parameters: Input
    Return: solution (JSON)
    """
    pulp.LpSolverDefault.msg = False

    # Define the problem
    prob = LpProblem("Truck_Loading_Problem", LpMinimize)

    # instantiate the solver
    number_of_products = input.numberOfProducts
    number_of_truck_types = input.numberOfTruckTypes
    product_volumes = input.productVolumes
    product_demand_quantity = input.productDemandQuantity
    truck_type_capacities = input.truckTypeCapacities
    number_of_trucks_per_type = input.numberOfTrucksPerType

    solver = Solver(numberOfProducts=number_of_products,
                    numberOfTruckTypes=number_of_truck_types,
                    prob=prob,
                    productVolumes=product_volumes,
                    productDemandQuantity=product_demand_quantity,
                    truckTypeCapacities=truck_type_capacities,
                    numberOfTrucksPerType=number_of_trucks_per_type
                    )

    # Solve the problem
    solution = solver.getSolution()
    return json.dumps(solution)
