Security
========
Security in Emelem is handled by Flask AppBuilder (FAB). FAB is a
"Simple and rapid application development framework, built on top of Flask.".
FAB provides authentication, user management, permissions and roles.


Provided Roles
--------------
Emlem ships with a set of roles that are handled by Emelem itself.
You can assume that these roles will stay up-to-date as Emelem evolves.
Even though it's possible for ``Admin`` users to do so, it is not recommended
that you alter these roles in any way by removing
or adding permissions to them as these roles will be re-synchronized to
their original values as you run your next ``emelem init`` command.

Since it's not recommended to alter the roles described here, it's right
to assume that your security strategy should be to compose user access based
on these base roles and roles that you create. For instance you could
create a role ``Data scientist`` that would be made of set of permissions
to a set of models (mlms).

Admin
"""""
Admins have all possible rights, including granting or revoking rights from
other users and altering other people's slices and dashboards.

Public
""""""
It's possible to allow logged out users to access some Emelem features.


Customizing
-----------

The permissions exposed by FAB are very granular and allow for a great level
of customization. FAB creates many permissions automatically for each model
that is create (can_add, can_delete, can_show, can_edit, ...) as well as for
each view. 

We do not recommend altering the 2 base roles as there
are a set of assumptions that Emelem build upon. It is possible though for
you to create your own roles, and union them to existing ones.

Permissions
"""""""""""

Roles are composed of a set of permissions, and Emelem has many categories
of permissions. Here are the different categories of permissions:

- **Model & action**: models are entities like ``MLM``,
  ``Project``, or ``User``. Each model has a fixed set of permissions, like
  ``can_edit``, ``can_show``, ``can_delete``, ``can_list``, ``can_add``, and
  so on. By adding ``can_delete on Project`` to a role, and granting that
  role to a user, this user will be able to delete projects.
- **Views**: views are individual web pages. When granted to a user, he/she will see that view in
  the its menu items, and be able to load that page.

