import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AppRoutingStateService {
  private sharedStateData: any = {};

  constructor() { }
  setSharedStateData(key: String, value: any) {
    this.sharedStateData.key = value;
  }

  getSharedStateData(key: String, valueIfNotFound?: any) {
    if (this.sharedStateData.hasOwnProperty(key)) {
      return this.sharedStateData.key;
    } else if (valueIfNotFound) {
      return valueIfNotFound;
    } else {
      console.log("Issue in routing state detected. This condition should not occur", key);
      return undefined;
    }
  }

  getRouteName(routeURL: String) {
    const segments = routeURL.split('/');
    return segments[segments.length - 1];
  }
}
