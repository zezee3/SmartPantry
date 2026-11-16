# SmartPantry Project Overview

## Project title

**SmartPantry: A Food Inventory and Expiration Tracking System**

## Project concept

SmartPantry is a web-based household tool for recording food supplies, tracking quantities, and reviewing recorded expiration dates. It gives users a single place to see what is in their pantry and which items may need attention.

## Problem being addressed

Households may forget which food items they already have or overlook dates printed on packaging. This can lead to unnecessary purchases and food being left unused. A simple inventory and reminder tool can make household food management more organized.

## General objective

To develop a web-based food inventory and expiration tracking system that helps household users organize pantry records and identify items that may need attention based on their recorded dates.

## Specific objectives

1. Allow users to add, view, edit, and delete food records.
2. Organize records by food category and quantity.
3. Compare recorded expiration dates with the current date.
4. Display items that are past their recorded date or approaching it.
5. Apply rule-based classification using Prolog.
6. Store pantry information in an SQLite database.
7. Demonstrate imperative, functional, logic, and object-oriented programming in one application.

## Intended users

The first version is designed for an individual or household managing a shared pantry on one local computer. Multi-user accounts and cloud synchronization are outside the initial scope.

## Main system features

| Feature | Description |
|---|---|
| Food inventory | Create, read, update, and delete pantry records. |
| Categories | Group items into common food categories. |
| Expiration tracker | Calculate the number of days until or since a recorded date. |
| Date status | Label an item as expired, expiring soon, fresh, or having no recorded date. |
| Priority label | Use Prolog rules to assign Review item, Use soon, or Normal. |
| Dashboard | Summarize records and highlight items that may need attention. |
| Search and filter | Find items by name or category. |

## UN Sustainable Development Goal alignment

**SDG 12: Responsible Consumption and Production** is the primary alignment. SmartPantry supports more mindful household food management by making existing supplies visible and highlighting dates that users may otherwise overlook. The system may help users plan how to use food they already have and reduce avoidable household waste. The application does not measure or prove a reduction in food waste; that would require a separate user evaluation.

## Scope and boundaries

Included:
- Local web application
- Pantry item records and quantity fields
- Optional recorded expiration date
- Date-based status and priority reminders
- SQLite persistence
- Prolog-based rule classification

Not included in this first version:
- Barcode scanning or image recognition
- Automatic online grocery ordering
- Payment processing
- Email or mobile push notifications
- Food safety diagnosis or guarantees
- User accounts, multiple households, or cloud hosting

## Assumptions

- Users enter accurate item names, quantities, and dates.
- The application uses the device's local date when calculating reminders.
- The default expiring-soon window is 0 to 3 days inclusive and can be changed in the Prolog rules.
- A date reminder is only an organizational aid. Users must check product labels, storage conditions, and food-safety guidance.
