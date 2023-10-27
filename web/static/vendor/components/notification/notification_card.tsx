"use strict";
import React from "react";

type NotificationHeaderProps = {
    category: string,
    newNotifications: number
    showDismissNumber: boolean
};

/**
 * NotificationHeader: The header for each notification card
 * @param category - The category of the notification
 * @param newNotifications - The number of new notifications in the category
 * @param showDismissNumber - Whether to show the number of new notifications
 *
 * @return - The header for the notification card
 */
const NotificationHeader = ({category, newNotifications, showDismissNumber}: NotificationHeaderProps) => {
    const title = `${category.charAt(0).toUpperCase()}${category.substring(1)} Notifications`;
    return (
        <div
            id={`accordion-header-${category}`}
            className={"card-header btn btn-link position-relative"}
            data-toggle={"collapse"}
            data-target={`#accordion-body-${category}`}
            aria-expanded={"false"}
            aria-controls={`accordion-body-${category}`}
        >
            <h2 className={"card-title"}>{title}</h2>
            {showDismissNumber && newNotifications > 0 &&
                <h5 className={"badge badge-primary card-badge"}>{newNotifications}</h5>
            }
        </div>
    );
};

type NotificationCardProps = {
    type: string
    children: React.ReactElement,
    newNotifNumber: number,
    showDismissBtn: boolean,
    dismissAll: (contentType: string) => void,
};

/**
 * NotificationCard: The card for each notification category
 * @param type - The category of the notification
 * @param newNotifNumber - The number of new notifications in the category
 * @param children - The React components to render in the card
 * @param showDismissBtn - Whether to show the dismiss all button
 * @param dismissAll - The function to dismiss all notifications in the category
 *
 * @return - The card for the notification category
 */
export const NotificationCard = ({type, newNotifNumber, children, showDismissBtn, dismissAll}: NotificationCardProps) => {
    return (
        <div className={"row mt-4 accordion"}>
            <div className={"card col px-0"}>
                <NotificationHeader category={type} showDismissNumber={showDismissBtn} newNotifications={newNotifNumber} />
                <div id={`accordion-body-${type}`} className={"collapse p-3"}>
                    {showDismissBtn &&
                        <div className={"d-flex justify-content-end"}>
                            <a className={"btn btn-link btn-outline float-right"} onClick={() => dismissAll(type)}>Dismiss all</a>
                        </div>
                    }
                    <div className={"card-body"}>
                        <div id={`form-container-${type}`} className={"card-text table-responsive"}>
                            { children }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
