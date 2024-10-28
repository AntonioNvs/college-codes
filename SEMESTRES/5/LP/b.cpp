void binary_search(int lo, int hi, int x){
    while(lo < hi){
        int mid = (lo + hi)/2; 
        if(v[i] >= x) mid = hi;
        else lo = mid+1;
    }
    return lo;
}

