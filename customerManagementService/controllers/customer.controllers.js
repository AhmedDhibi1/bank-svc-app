const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
require("dotenv").config();
const Customer = require("../models/customer");

async function getAll(req, res) {
  try {
    return await Customer.findAll();
  } catch (err) {
    throw new Error("Error fetching customers");
  }
}
async function getById(id) {
  return await Customer.findByPk(id);
}
async function create(customerParam) {
  if (!customerParam || !customerParam.email || !customerParam.password) {
    throw "Invalid customer parameters provided";
  }

  const existingCustomer = await Customer.findOne({
    where: { email: customerParam.email },
  });
  if (existingCustomer) {
    throw `This email already exists: ${customerParam.email}`;
  }

  const hashedPassword = bcrypt.hashSync(customerParam.password, 10);
  await Customer.create({
    name: customerParam.name,
    address: customerParam.address,
    phone: customerParam.phone,
    email: customerParam.email,
    password: hashedPassword,
  });
}

async function update(id, customerParam) {
  console.log("customerParam:", customerParam);
  const customer = await Customer.findByPk(id);
  if (!customer) {
    throw "Customer not found.";
  }

  if (customer.email !== customerParam.email) {
    const existingCustomer = await Customer.findOne({
      where: { email: customerParam.email },
    });
    if (existingCustomer) {
      throw `Customer with email ${customerParam.email} already exists.`;
    }
  }

  if (customerParam.password) {
    customerParam.password = bcrypt.hashSync(customerParam.password, 10);
  }

  await customer.update(customerParam);
  console.log("Customer:", customer);
  console.log("Customer with id:", id, "updated successfully.");
}

async function _delete(customerId) {
  await Customer.destroy({
    where: {
      id: customerId,
    },
  });

  console.log(
    "---------------------------Customer with id:",
    customerId,
    "deleted successfully."
  );
}

module.exports = {
  getAll,
  getById,
  create,
  update,
  delete: _delete,
};
