# -*- coding: utf-8 -*-
"""
Created on Sun May 12 20:17:17 2019

@author: syuntoku
"""

import adsk, re
from xml.etree.ElementTree import Element, SubElement
from ..utils import utils


def normalize_link_name(name):
    """
    Converts Fusion 360 occurrence names into stable URDF link names.

    Examples:
        base_link v1:1 -> base_link
        link1 v1:1     -> link1
        link2 v2:3     -> link2
    """

    name = name.replace(":", "_")
    name = name.replace(" ", "_")

    # Remove Fusion version suffixes
    name = re.sub(r"_v\d+_\d+$", "", name)

    # Collapse repeated underscores
    name = re.sub(r"_+", "_", name)

    return name.strip("_")


class Joint:

    def __init__(self, name, xyz, axis, parent, child, joint_type, upper_limit, lower_limit):

        self.name = name
        self.type = joint_type
        self.xyz = xyz
        self.parent = normalize_link_name(parent)
        self.child = normalize_link_name(child)
        self.joint_xml = None
        self.tran_xml = None
        self.axis = axis
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit


    def make_joint_xml(self):

        joint = Element('joint')
        joint.attrib = {
            'name': self.name,
            'type': self.type
        }

        origin = SubElement(joint, 'origin')
        origin.attrib = {
            'xyz': ' '.join([str(_) for _ in self.xyz]),
            'rpy': '0 0 0'
        }

        parent = SubElement(joint, 'parent')
        parent.attrib = {
            'link': self.parent
        }

        child = SubElement(joint, 'child')
        child.attrib = {
            'link': self.child
        }

        if self.type in ['revolute', 'continuous', 'prismatic']:

            axis = SubElement(joint, 'axis')
            axis.attrib = {
                'xyz': ' '.join([str(_) for _ in self.axis])
            }

        if self.type in ['revolute', 'prismatic']:

            limit = SubElement(joint, 'limit')
            limit.attrib = {
                'upper': str(self.upper_limit),
                'lower': str(self.lower_limit),
                'effort': '100',
                'velocity': '100'
            }

        self.joint_xml = "\n".join(
            utils.prettify(joint).split("\n")[1:]
        )


    def make_transmission_xml(self):

        tran = Element('transmission')
        tran.attrib = {
            'name': self.name + '_tran'
        }

        joint_type = SubElement(tran, 'type')
        joint_type.text = 'transmission_interface/SimpleTransmission'

        joint = SubElement(tran, 'joint')
        joint.attrib = {
            'name': self.name
        }

        hardwareInterface_joint = SubElement(
            joint,
            'hardwareInterface'
        )

        hardwareInterface_joint.text = (
            'hardware_interface/EffortJointInterface'
        )

        actuator = SubElement(tran, 'actuator')
        actuator.attrib = {
            'name': self.name + '_actr'
        }

        hardwareInterface_actr = SubElement(
            actuator,
            'hardwareInterface'
        )

        hardwareInterface_actr.text = (
            'hardware_interface/EffortJointInterface'
        )

        mechanicalReduction = SubElement(
            actuator,
            'mechanicalReduction'
        )

        mechanicalReduction.text = '1'

        self.tran_xml = "\n".join(
            utils.prettify(tran).split("\n")[1:]
        )


def make_joints_dict(root, msg):

    joint_type_list = [
        'fixed',
        'revolute',
        'prismatic',
        'Cylinderical',
        'PinSlot',
        'Planner',
        'Ball'
    ]

    joints_dict = {}

    for joint in root.joints:

        joint_dict = {}

        joint_type = joint_type_list[
            joint.jointMotion.jointType
        ]

        joint_dict['type'] = joint_type

        joint_dict['axis'] = [0, 0, 0]
        joint_dict['upper_limit'] = 0.0
        joint_dict['lower_limit'] = 0.0


        if joint_type == 'revolute':

            joint_dict['axis'] = [
                round(i, 6)
                for i in joint.jointMotion.rotationAxisVector.asArray()
            ]

            max_enabled = (
                joint.jointMotion.rotationLimits.isMaximumValueEnabled
            )

            min_enabled = (
                joint.jointMotion.rotationLimits.isMinimumValueEnabled
            )


            if max_enabled and min_enabled:

                joint_dict['upper_limit'] = round(
                    joint.jointMotion.rotationLimits.maximumValue,
                    6
                )

                joint_dict['lower_limit'] = round(
                    joint.jointMotion.rotationLimits.minimumValue,
                    6
                )


            elif max_enabled and not min_enabled:

                msg = (
                    joint.name +
                    ' is not set its lower limit. Please set it and try again.'
                )
                break


            elif not max_enabled and min_enabled:

                msg = (
                    joint.name +
                    ' is not set its upper limit. Please set it and try again.'
                )
                break


            else:

                joint_dict['type'] = 'continuous'


        elif joint_type == 'prismatic':

            joint_dict['axis'] = [
                round(i, 6)
                for i in joint.jointMotion.slideDirectionVector.asArray()
            ]


        # Parent and child links
        joint_dict['parent'] = normalize_link_name(
            joint.occurrenceTwo.name
        )

        joint_dict['child'] = normalize_link_name(
            joint.occurrenceOne.name
        )


        def trans(M, a):

            ex = [M[0], M[4], M[8]]
            ey = [M[1], M[5], M[9]]
            ez = [M[2], M[6], M[10]]
            oo = [M[3], M[7], M[11]]

            b = [0, 0, 0]

            for i in range(3):
                b[i] = (
                    a[0]*ex[i] +
                    a[1]*ey[i] +
                    a[2]*ez[i] +
                    oo[i]
                )

            return b


        def allclose(v1, v2, tol=1e-6):

            return max(
                [abs(a-b) for a, b in zip(v1, v2)]
            ) < tol


        try:

            xyz_from_one_to_joint = (
                joint.geometryOrOriginOne.origin.asArray()
            )

            xyz_from_two_to_joint = (
                joint.geometryOrOriginTwo.origin.asArray()
            )

            xyz_of_one = (
                joint.occurrenceOne.transform.translation.asArray()
            )

            xyz_of_two = (
                joint.occurrenceTwo.transform.translation.asArray()
            )

            M_two = (
                joint.occurrenceTwo.transform.asArray()
            )


            case1 = allclose(
                xyz_from_two_to_joint,
                xyz_from_one_to_joint
            )

            case2 = allclose(
                xyz_from_two_to_joint,
                xyz_of_one
            )


            if case1 or case2:

                xyz_of_joint = xyz_from_two_to_joint

            else:

                xyz_of_joint = trans(
                    M_two,
                    xyz_from_two_to_joint
                )


            joint_dict['xyz'] = [
                round(i / 100.0, 6)
                for i in xyz_of_joint
            ]


        except:

            msg = (
                joint.name +
                " doesn't have joint origin. Please set it and run again."
            )
            break


        joints_dict[joint.name] = joint_dict


    return joints_dict, msg