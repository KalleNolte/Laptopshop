interface screenResolutionSize {
  [index: number]: number;
}
interface productDimension {
  [index: number]: number;
}

export interface Laptop {
  asin: string;
  productTitle: string; 
  price: number;
  displaySize: number;
  screenResoultionSize: screenResolutionSize;
  processorSpeed: number;
  processorType: string;
  processorCount: number;
  processorBrand: string;
  ram: number;
  brandName: string;
  hardDriveType: string;
  hardDriveSize: number;
  graphicsCoprocessor: string;
  chipsetBrand: string;
  operatingSystem: string;
  itemWeight: number;
  memoryType: string;
  averageBatteryLife: number;
  productDimension: productDimension;
  color: string;
  imagePath: string;
  avgRating: number;

}

// export class Laptop {
//   constructor(
//     asin ?: string,
//     productTitle ?: string, 
//     price ?: number,
//     displaySize ?: number,
//     screenResoultionSize ?: screenResolutionSize,
//     processorSpeed ?: number,
//     processorType ?: string,
//     processorCount ?: number,
//     processorBrand ?: string,
//     ram ?: number,
//     brandName ?: string,
//     hardDriveType ?: string,
//     hardDriveSize ?: number,
//     graphicsCoprocessor ?: string,
//     chipsetBrand ?: string,
//     operatingSystem ?: string,
//     itemWeight ?: number,
//     memoryType ?: string,
//     averageBatteryLife ?: number,
//     productDimension ?: productDimension,
//     color ?: string,
//     imagePath ?: string,
//     avgRating ?: number,
//   ) {}
//}
